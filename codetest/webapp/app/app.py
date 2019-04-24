from flask import render_template, request, Blueprint
from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField, SelectField
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

    target_date = DateTimeField("Target Date", id="datepick")
    client = QuerySelectField(
        query_factory=lambda: Client.query.all(),
        get_pk=lambda a: a.id,
        get_label=lambda a: a.name,
        allow_blank=False,
        blank_text=u"-- please choose --",
    )
    priority = SelectField(
        choices=Priority.PRIORITIES,
        coerce=choice_type_coerce_factory(Priority.value.type),
        validators=[DataRequired()],
    )
    product_area = SelectField(
        choices=ProductArea.AREAS,
        coerce=choice_type_coerce_factory(ProductArea.name.type),
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

    return render_template("index.html", form=form)
