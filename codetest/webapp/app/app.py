from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateTimeField,
    TextAreaField,
    SubmitField,
    BooleanField,
    PasswordField,
)
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap

from .models import db, FeatureRequest
from . import create_app

app = create_app()

bootstrap = Bootstrap(app)


class RequestFeatureForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(1, 20)])
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(8, 150)]
    )
    target_date = DateTimeField("Target Date", id="datepick")
    submit = SubmitField()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form")
def form():
    form = RequestFeatureForm()
    return render_template("form.html", form=form)
