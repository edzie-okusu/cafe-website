import requests
from flask import Flask, render_template, redirect, url_for, flash, request, g, abort
from flask_sqlalchemy import SQLAlchemy
import random
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

app = Flask(__name__)
API_KEY = 'TopSecretApi'

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Cafe and Wifi Website Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

class Member(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class MemberForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Your E-mail Address', validators=[DataRequired(), Email()])
    number = StringField('Your telephone number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()], Length(min=8, max=20))
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password', message='Passwords must match')])
    sign_up = SubmitField("Sign Me Up")

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location', validators=[DataRequired(), URL()])
    img_url= StringField('Image Link of Place', validators=[DataRequired()])
    map_url=StringField('Google Map Address', validators=[DataRequired()])
    wifi_availability = SelectField('Is wifi available?', choices=[('0','No'),('1','Yes')], validators=[DataRequired()])
    powersocket_availability = SelectField('Are Power Sockets readily available', choices=[('1','Yes'),('0', 'No')], validators=[DataRequired()])
    can_take_calls = SelectField('Customers can receive calls?', choices=[('1','Yes'),('0', 'No')], validators=[DataRequired()])
    toilets = SelectField('Do they have Sanitary Restrooms', choices=[('1','Yes'),('0', 'No')], validators=[DataRequired()])
    coffee_price = StringField('Price of Coffee', validators=[DataRequired()])
    seats = SelectField('Are the available seats sufficient?', choices=[('1','Yes'),('0', 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

with app.app_context():
    db.create_all()

@app.route("/homepage")
def home():
    return render_template("index.html")

@app.route('/about_cafe_and_wifi')
def about():
    return render_template('about.html')


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        name = form.cafe.data
        location = form.location.data
        wifi = form.wifi_availability.data
        sockets = form.powersocket_availability.data
        img_url = form.img_url.data
        map_url=form.map_url.data
        toilets= form.toilets.data
        seats= form.seats.data
        coffee_price = form.coffee_price.data 
        can_take_calls=form.can_take_calls.data


        new_cafe = Cafe(
            name=name, 
            map_url=map_url, 
            location=location,  
            img_url=img_url, 
            has_wifi=wifi, 
            seats=seats, 
            has_toilet=toilets, 
            has_sockets=sockets, 
            can_take_calls=can_take_calls
            )
        db.session.add(new_cafe)
        db.session.commit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.all()
    return render_template('cafes.html', cafes=all_cafes)

#app.route('/join_the_community')
def join():
    form = MemberForm()
    if form.validate_on_submit():
        name = form.name.data 
        email = form.email.data
        number = form.number.data 
        hashed_password = generate_password_hash(form.password.data)
        new_member = Member(
            name = name,
            email = email,
            telephone = number,
            password = hashed_password
            )
        db.session.add(new_member)
        db.session.commit()
        return render_template('message.html', message = "You've joined the community. Welcome!")
    return render_template('signup.html', form=form)
