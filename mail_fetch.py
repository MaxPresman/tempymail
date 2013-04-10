from smtpd import SMTPServer
import asyncore
import email
from sqlalchemy import select
import orm

class TempySMTPserver(SMTPServer):
   def process_message(self, peer, mailfrom, rcpttos, data):
		conn   			= orm.engine.connect()
		
		#print "peer "    + str(peer		)
		#print "mailfrom" + str(mailfrom	)
		#print "rcpttos:" + str(rcpttos	)
		#print "data"	 + str(data)
		
		parsed_email	= email.message_from_string(data)
		
		for email_recpt in rcpttos:
			email_username = email_recpt.split("@")[0]
			
			print email_username

			##find the account
			existing_account	= conn.execute(select([orm.email_account]).where(orm.email_account.c.inbox_name == email_username)).first()
			
			if not existing_account: continue
					
			pay_loads =  parsed_email.get_payload()

			if type(pay_loads) != list:
				pay_loads = [pay_loads]

			insert_me 										= {}
			insert_me[orm.emails_recieved.c.owner_id] 		= existing_account.id
			insert_me[orm.emails_recieved.c.email_title] 	= parsed_email["Subject"]
			insert_me[orm.emails_recieved.c.email_from]		= mailfrom

			for recieved_email_type in pay_loads:
				if type(recieved_email_type) == str and parsed_email.get_content_type() == "text/plain":
					insert_me[orm.emails_recieved.c.email_desc_plain] = recieved_email_type
				elif type(recieved_email_type) == str and parsed_email.get_content_type() == "text/html":
					insert_me[orm.emails_recieved.c.email_desc_html] = recieved_email_type
				elif recieved_email_type.get_content_type() == "text/plain": 
					insert_me[orm.emails_recieved.c.email_desc_plain] = recieved_email_type.get_payload()
				elif recieved_email_type.get_content_type() == "text/html": 
					insert_me[orm.emails_recieved.c.email_desc_html] = recieved_email_type.get_payload()

			insert_statement = orm.emails_recieved.insert().values(insert_me)
			conn.execute(insert_statement)

		conn.close()


smtp_obj = TempySMTPserver(('0.0.0.0', 25), None)

try:
	   asyncore.loop()
except KeyboardInterrupt:
	   pass