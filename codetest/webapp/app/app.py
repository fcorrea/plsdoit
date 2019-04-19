from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap

from .models import db, FeatureRequest
from . import create_app

app = create_app()

bootstrap = Bootstrap(app)


class HelloForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField("Remember me")
    submit = SubmitField()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form")
def form():
    form = HelloForm()
    return render_template("form.html", form=form)
