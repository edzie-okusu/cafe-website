# import requests
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import random

from sqlalchemy import func

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Cafe and Wifi Website Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'TopSecretApi'
db = SQLAlchemy(app)
Bootstrap(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location', validators=[DataRequired(), URL()])
    img_url = StringField('Image Link of Place', validators=[DataRequired()])
    map_url = StringField('Google Map Address', validators=[DataRequired()])
    wifi_availability = SelectField('Is wifi available?', choices=[('0', 'No'), ('1', 'Yes')],
                                    validators=[DataRequired()])
    powersocket_availability = SelectField('Are Power Sockets readily available', choices=[('1', 'Yes'), ('0', 'No')],
                                           validators=[DataRequired()])
    can_take_calls = SelectField('Customers can receive calls?', choices=[('1', 'Yes'), ('0', 'No')],
                                 validators=[DataRequired()])
    toilets = SelectField('Do they have Sanitary Restrooms', choices=[('1', 'Yes'), ('0', 'No')],
                          validators=[DataRequired()])
    coffee_price = StringField('Price of Coffee', validators=[DataRequired()])
    seats = SelectField('Are the available seats sufficient?', choices=[('1', 'Yes'), ('0', 'No')],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            print("True")
            name = form.cafe.data
            location = form.location.data
            wifi = form.wifi_availability.data
            sockets = form.powersocket_availability.data
            img_url = form.img_url.data
            map_url = form.map_url.data
            toilets = form.toilets.data
            seats = form.seats.data
            coffee_price = form.coffee_price.data
            can_take_calls = form.can_take_calls.data

            new_cafe = Cafe(
                name=name,
                map_url=map_url,
                location=location,
                img_url=img_url,
                has_wifi=wifi,
                seats=seats,
                has_toilet=toilets,
                has_sockets=sockets,
                can_take_calls=can_take_calls,
                coffee_price=coffee_price
            )
            db.session.add(new_cafe)
            db.session.commit()
    return render_template('new_cafe.html', form=form)


@app.route('/all_cities')
def all_cities():
    return render_template('all_places.html')

@app.route('/ldn/cafes')
def london_cafes():
    all_cafes = Cafe.query.all()
    return render_template('city.html', cafes=all_cafes)


@app.route('/cafe/<int:index>')
def cafe(index):
    cafe_id = index
    search_cafe = Cafe.query.filter_by(cafe_id).first()
    if search_cafe:
        return render_template('cafe.html', cafe_data=search_cafe)



if __name__ == "__main__":
    app.run(debug=True)
