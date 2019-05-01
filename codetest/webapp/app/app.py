from flask import render_template, request, Blueprint, jsonify
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms_components.fields import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms_alchemy import model_form_factory, ModelFormField, QuerySelectField
from wtforms_alchemy.utils import choice_type_coerce_factory

from .models import db, FeatureRequest, Client, ProductArea

features = Blueprint("features", __name__, template_folder="templates")

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class RequestFeatureForm(ModelForm):
    class Meta:
        model = FeatureRequest

    target_date = DateField("Target Date", id="datepick", format="%m/%d/%Y")
    client_id = SelectField(
        "Client", choices=Client.CLIENTS, coerce=int, validators=[DataRequired()]
    )
    client_priority = IntegerField(validators=[NumberRange(min=1)])
    product_area_id = SelectField(
        "Product Area",
        choices=ProductArea.AREAS,
        coerce=int,
        validators=[DataRequired()],
    )
    submit = SubmitField()


@features.route("/")
def index():
    form = RequestFeatureForm()
    return render_template("index.html", form=form)


@features.route("/new", methods=["POST"])
def new():
    form = RequestFeatureForm()
    if form.validate_on_submit():
        client_id = form.client_id.data
        client_priority = form.client_priority.data
        existing = (
            db.session.query(FeatureRequest)
            .filter(
                FeatureRequest.client_id == client_id,
                FeatureRequest.client_priority == client_priority,
            )
            .order_by(FeatureRequest.client_priority)
        )
        if existing.count() == 1:
            # Check for gaps
            gap = (
                db.session.query(FeatureRequest)
                .filter(
                    FeatureRequest.client_id == client_id,
                    FeatureRequest.client_priority == client_priority + 1,
                )
                .count()
            )
            reset_priority(
                client_id, base_priority=client_priority, propagate=bool(gap)
            )

        feature_request = FeatureRequest()
        form.populate_obj(feature_request)
        db.session.add(feature_request)
        db.session.commit()

    return jsonify(form.errors)


@features.route("/delete", methods=["POST"])
def delete():
    message = {"message": "success"}
    feature_request_id = request.form.get("feature_request_id")
    result = (
        db.session.query(FeatureRequest)
        .filter(FeatureRequest.id == feature_request_id)
        .delete()
    )
    if result:
        message = {"message": "Successfully created new feature request"}
    else:
        message = {"message": "Could not delete feature request"}
    db.session.commit()
    return jsonify(message)


@features.route("/edit", methods=["POST"])
def edit():
    id = request.form.get("feature_request_id")
    feature_request = FeatureRequest.query.get_or_404(id)
    form = RequestFeatureForm(obj=feature_request)
    message = {"message": u"Successfully changed feature request."}
    if form.validate_on_submit():
        client_id = form.client_id.data
        client_priority = form.client_priority.data
        existing = (
            db.session.query(FeatureRequest)
            .filter(
                FeatureRequest.client_id == client_id,
                FeatureRequest.client_priority == client_priority,
                FeatureRequest.id != id,
            )
            .order_by(FeatureRequest.client_priority)
        )
        if existing.count() == 1:
            # Check for gaps
            gap = (
                db.session.query(FeatureRequest)
                .filter(
                    FeatureRequest.client_id == client_id,
                    FeatureRequest.client_priority == client_priority + 1,
                )
                .count()
            )
            reset_priority(
                client_id, base_priority=client_priority, propagate=bool(gap)
            )
            message["message"] += u" Client priority was reset."

        form.populate_obj(feature_request)
        db.session.commit()

    return jsonify(message)


def reset_priority(client_id, base_priority=None, propagate=False):
    """Reset priority of ``FeatureRequest``s using ``base_priority``.

    When ``propagate`` is ``True``, all records will have their ``client_priority``
    bumped. 
    """
    reach = (
        FeatureRequest.client_priority >= base_priority
        if propagate
        else FeatureRequest.client_priority == base_priority
    )
    db.session.query(FeatureRequest).filter(
        FeatureRequest.client_id == client_id, reach
    ).update({FeatureRequest.client_priority: FeatureRequest.client_priority + 1})
    db.session.commit()
