from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
#Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY']="INVISIBLE KEY"

#Create a form class
class NamerForm(FlaskForm):
	name = StringField("What's your Name?",validators=[DataRequired()])
	submit = SubmitField("Submit")



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
	return render_template('name.html',name=name,form=form)

