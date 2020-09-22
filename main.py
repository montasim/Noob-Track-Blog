#    ------------------------------------------------------------------------------------------
#    Author    : Mohammad Montasim -Al- Mamun Shuvo
#    Copyright : Copyright 2020, Mohammad Montasim -Al- Mamun Shuvo
#    Email     : montasimmamun@gmail.com
#    Github    : https://github.com/montasimmamun/

#    Date      : Created on 17/08/2020
#    Version   : 1.0.1
#    Purpose   : Learn Flask
#    Input     : None
#    Output    : Flask App Output
#    ------------------------------------------------------------------------------------------


from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import os
import json

with open('D:\PROFESSIONAL\CODES\PYTHON\[Hindi] Web Development Using Flask and Python\config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__)

#   send email using gmail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_username'],
    MAIL_PASSWORD=params['gmail_password'],
)

mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

db = SQLAlchemy(app)

#   Serial_No, Name, Email, Phone, Message, Contact_Date


class Contacts(db.Model):
    Serial_No = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(20), nullable=False)
    Phone = db.Column(db.String(12), nullable=False)
    Message = db.Column(db.String(120), nullable=False)
    Contact_Date = db.Column(db.String(12), nullable=True)


#   Serial_No, Post_Title, Slug, Content, Post_Date
class Post(db.Model):
    Serial_No = db.Column(db.Integer, primary_key=True)
    Post_Title = db.Column(db.String(80), nullable=False)
    Slug = db.Column(db.String(50), nullable=False)
    Content = db.Column(db.String(200), nullable=False)
    Post_Date = db.Column(db.String(12), nullable=True)
    Img_File = db.Column(db.String(12), nullable=True)


@app.route('/')
def index():
    return render_template('index.html', params=params)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(Slug=post_slug).first()
    return render_template('post.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html', params=params, post=post)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if(request.method == 'POST'):

        #   add entry to database
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        #   Serial_No, Name, Email, Phone, Message, Contact_Date
        entry = Contacts(Name=name, Email=email, Phone=phone,
                         Message=message, Contact_Date=datetime.now())

        db.session.add(entry)
        db.session.commit()
        mail.send_message('New Message From ' + name,
                          sender=email,
                          recipients=[params['gmail_username']],
                          body=message + "\n"
                          + "Email : " + email + "\n"
                          + "Phone : " + phone
                          )

    return render_template('contact.html', params=params)


#   app.run() function run flask app & gives an external link
#   debug=True automatically run flask app when it is saved
app.run(debug=True)
