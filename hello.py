from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

#Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY']="INVISIBLE KEY"
#add database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'

#Initialize the database
db = SQLAlchemy(app)

#set timezone
tz = pytz.timezone('Asia/Kolkata')
date_time=datetime.now(tz)

#Create a model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow())

	def __repr__(self):
		return '<Name %r>' % self.name
	

#Create a form class
class NamerForm(FlaskForm):
	name = StringField("What's your Name?",validators=[DataRequired()])
	submit = SubmitField("Submit")

#Creating a user form:
#Create a form class
class UserForm(FlaskForm):
	name = StringField("Name",validators=[DataRequired()])
	email= StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Enter")




#Create rout decorator
@app.route('/')
# def index():
#     return "<h1>Hello World!!<h1>"

def index():
	favourite_pizza=["Tandoori","Paneer","Spicy","Onion"]
	return render_template("index.html",favourite_pizza=favourite_pizza)

@app.route('/user/<name>')
def user(name):
	return render_template("user.html",user_name=name)

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"),500

#Create Nmae Page
@app.route('/name',methods=['GET','POST'])
def name():
	name=None
	form=NamerForm()
	#Validate
	if form.validate_on_submit():
		name=form.name.data
		form.name.data=''
		flash("Form Submitted Successfully!!")
	return render_template('name.html',name=name,form=form)

@app.route('/user/add', methods=['GET','POST'])
def add_user():
	form=UserForm()
	name =None
	email= None
	if(form.validate_on_submit()):
		name=form.name.data
		user = Users.query.filter_by(email=form.email.data).first()#return the first user of all the users with the same email address 
		if user is None:#is there is no user with the given email id put him in the database
			user = Users(name=form.name.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
			flash('User added Successfully')
		else:
			flash('User email already registered')
		form.name.data=''
		form.email.data=''
	our_users=Users.query.order_by(Users.date_added)
	return render_template("add_user.html",form=form,name=name,our_users=our_users)
