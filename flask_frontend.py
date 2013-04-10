from flask import Flask
from flask import render_template,redirect,request,session,url_for
import json
import datetime
import os
import random
import string
import settings as external_settings

from sqlalchemy import select
import orm

app = Flask(__name__)


@app.route('/')
def index_page():
	## make a new email and redirect to the box
	new_email,new_access_key 	= make_new_email_address()
	new_url 					= url_for('show_email_account',email_secret=new_access_key)
	return redirect(new_url)


@app.route('/mail/<email_secret>')
def show_email_account(email_secret):
	
	conn   				= orm.engine.connect()
	existing_account	= conn.execute(select([orm.email_account]).where(orm.email_account.c.access_key == email_secret)).first()
	
	if not existing_account:
		return render_template("index.htm",error="email_not_found")

	existing_mail		= conn.execute(select([orm.emails_recieved]).where(orm.emails_recieved.c.owner_id == existing_account.id) )
	existing_mail 		= existing_mail.fetchall()

	return render_template("index.htm",email_account=existing_account,existing_mail=existing_mail,email_domain=external_settings.DOMAIN)

def make_new_email_address():

	conn   				= orm.engine.connect()
	empty_email_found 	= False

	while not empty_email_found:
		random_email = make_random()
		if conn.execute(select([orm.email_account]).where(orm.email_account.c.inbox_name == random_email)).rowcount == 0:
			empty_email_found = True
	
	access_key = make_random(16)

	insert_statement = orm.email_account.insert().values(inbox_name=random_email,access_key=access_key)
	conn.execute(insert_statement)

	return random_email,access_key



def make_random(def_len=8):
	import random,string
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(def_len))

if __name__ == "__main__":
	app.run(debug=True,port=3005,host="0.0.0.0")