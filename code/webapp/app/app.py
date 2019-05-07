from flask import render_template, request, Blueprint, jsonify
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms_components.fields import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms_alchemy import model_form_factory, ModelFormField, QuerySelectField
from wtforms_alchemy.utils import choice_type_coerce_factory
from sqlalchemy import func

from .models import FeatureRequest, Client, ProductArea
from .database import db_session
from .pagination import QueryPagination

features = Blueprint("features", __name__, template_folder="templates")

BaseModelForm = model_form_factory(FlaskForm)

DEFAULT_LIMIT = 5


SORTING_MAP = {
    "title": FeatureRequest.title,
    "client": FeatureRequest.client_id,
    "client_priority": FeatureRequest.client_priority,
}


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        from .database import db_session

        return db_session


class RequestFeatureForm(ModelForm):
    class Meta:
        model = FeatureRequest

    target_date = DateField("Target Date", id="datepick", format="%m/%d/%Y")
    client_id = SelectField(
        "Client", choices=Client.TYPES, coerce=int, validators=[DataRequired()]
    )
    client_priority = IntegerField(default=1, validators=[NumberRange(min=1)])
    product_area_id = SelectField(
        "Product Area",
        choices=ProductArea.TYPES,
        coerce=int,
        validators=[DataRequired()],
    )
    submit = SubmitField()


@features.route("/")
def index():
    form = RequestFeatureForm()
    client_counts = get_features_counts_by_client()
    priority_counts = get_priority_counts()

    return render_template(
        "index.html",
        form=form,
        client_counts=client_counts,
        priority_counts=priority_counts,
    )


@features.route("/new", methods=["POST"])
def new():
    form = RequestFeatureForm()
    if form.validate_on_submit():
        client_id = form.client_id.data
        client_priority = form.client_priority.data
        existing = (
            db_session.query(FeatureRequest)
            .filter(
                FeatureRequest.client_id == client_id,
                FeatureRequest.client_priority == client_priority,
            )
            .order_by(FeatureRequest.client_priority)
        )
        if existing.count() == 1:
            reset_priority(client_id, base_priority=client_priority)

        feature_request = FeatureRequest()
        form.populate_obj(feature_request)
        db_session.add(feature_request)
        db_session.commit()

    return jsonify(form.errors)


@features.route("/delete", methods=["POST"])
def delete():
    message = {"status": "success"}
    feature_request_id = request.form.get("id")
    result = (
        db_session.query(FeatureRequest)
        .filter(FeatureRequest.id == feature_request_id)
        .delete()
    )
    if result:
        message = {"status": "Successfully deleted new feature request"}
    else:
        message = {"status": "Could not delete feature request"}
    db_session.commit()
    return jsonify(message)


@features.route("/edit", methods=["POST"])
def edit():
    id = request.form.get("feature_request_id")
    feature_request = FeatureRequest.query.get(id)
    form = RequestFeatureForm(obj=feature_request)
    message = {"status": u"Successfully changed feature request."}
    if form.validate_on_submit():
        client_id = form.client_id.data
        client_priority = form.client_priority.data
        existing = (
            db_session.query(FeatureRequest)
            .filter(
                FeatureRequest.client_id == client_id,
                FeatureRequest.client_priority == client_priority,
                FeatureRequest.id != id,
            )
            .order_by(FeatureRequest.client_priority)
        )
        if existing.count() == 1:
            reset_priority(client_id, base_priority=client_priority)
            message["status"] += u" Client priority was reset."

        form.populate_obj(feature_request)
        db_session.commit()

    return jsonify(message)


@features.route("/list", methods=["GET"])
def list():
    """Check for query string parameters and return a list of feature requests"""
    params = request.args.to_dict()
    page = int(params.pop("page", 1))
    limit = int(params.pop("limit", 5))
    title = params.pop("title", None)
    sort_on = params.pop("sortBy", None)
    sort_direction = params.pop("direction", None)

    order = None
    if sort_on is not None:
        order = getattr(SORTING_MAP[sort_on], sort_direction)()

    if title is not None:
        feature_requests = FeatureRequest.query.filter(
            FeatureRequest.title.like("%{}%".format(title))
        )
    else:
        feature_requests = FeatureRequest.query.filter_by(**params).order_by(order)

    feature_requests = QueryPagination(feature_requests).paginate(
        page=page, per_page=limit
    )

    result = [i.serialize for i in feature_requests.items]
    return jsonify(records=result, total=feature_requests.total)


def reset_priority(client_id, base_priority=None):
    """Reset priority of ``FeatureRequest``s using ``base_priority``."""
    # Check for gaps
    gap = FeatureRequest.query.filter(
        FeatureRequest.client_id == client_id,
        FeatureRequest.client_priority == base_priority + 1,
    ).count()
    reach = (
        FeatureRequest.client_priority >= base_priority
        if gap
        else FeatureRequest.client_priority == base_priority
    )
    FeatureRequest.query.filter(FeatureRequest.client_id == client_id, reach).update(
        {FeatureRequest.client_priority: FeatureRequest.client_priority + 1}
    )
    db_session.commit()


def get_features_counts_by_client():
    """Creates a mapping between clients and all its feature counts"""
    feature_counts = (
        db_session.query(
            FeatureRequest.client_id,
            func.count(FeatureRequest.client_id).label("count"),
        )
        .group_by(FeatureRequest.client_id)
        .subquery()
    )
    counts = (
        db_session.query(Client.name, Client.id, feature_counts.c.count)
        .join(feature_counts, feature_counts.c.client_id == Client.id)
        .order_by(feature_counts.c.count.desc())
        .all()
    )

    result = []
    for client, client_id, count in counts:
        data = {}
        data["name"] = client
        data["id"] = client_id
        data["count"] = count
        result.append(data)

    return result


def get_css_badge(severity):
    """Map severity to a Bootstrap 4 css badge"""
    badges = ["badge badge-danger count", "badge badge-info count"]
    severities = [[1, 2, 3], [4, 5, 6, 7]]
    for index, severity_list in enumerate(severities):
        if severity in severity_list:
            return badges[index]
    else:
        return "badge badge-light count"


def get_priority_counts():
    """
    Get counts for all priority counts and return a dictionary that includes a css
    helper.
    """
    counts = (
        db_session.query(
            FeatureRequest.client_priority, func.count(FeatureRequest.client_priority)
        )
        .group_by(FeatureRequest.client_priority)
        .order_by(FeatureRequest.client_priority)
        .all()
    )

    result = []
    for priority, count in counts:
        data = {}
        badge = get_css_badge(priority)
        data["priority"] = priority
        data["count"] = count
        data["css_badge"] = badge
        result.append(data)

    return result
