from flask import render_template, request, Blueprint
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import model_form_factory, ModelFormField, QuerySelectField
from wtforms_alchemy.utils import choice_type_coerce_factory

from .models import db, FeatureRequest, Client, Priority, ProductArea

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
    client_priority_id = SelectField(
        "Priority", choices=Priority.PRIORITIES, coerce=int, validators=[DataRequired()]
    )
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
        feature_request = FeatureRequest()
        form.populate_obj(feature_request)
        db.session.add(feature_request)
        db.session.commit()
    return render_template("index.html", form=form)
