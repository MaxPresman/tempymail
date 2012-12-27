from smtpd import SMTPServer
import asyncore
import orm as ORM
import email


class my_smtp(SMTPServer):
   def process_message(self, peer, mailfrom, rcpttos, data):

		##connect to db
		ORM.database_go.connect()
		
		##prase the msg
		
		#print "peer "    + str(peer		)
		#print "mailfrom" + str(mailfrom	)
		print "rcpttos:" + str(rcpttos	)
		#print "data"	 + str(data)
		
		parsed_email	= email.message_from_string(data)
		print parsed_email.__dict__
		
		for email_recpt in rcpttos:
			email_username = email_recpt.split("@")[0]
			
			##find the account
			email_account 	= ORM.email_account.select().filter(inbox_name=email_username)
			email_account	= list(email_account)
			
			if not email_account: continue
			
			email_account 	= email_account[0]
			
			save_new_email 				= ORM.emails_recieved()
			save_new_email.email_title 	= parsed_email["Subject"]
			save_new_email.owner		= email_account
			save_new_email.email_desc	= parsed_email.get_payload()
			save_new_email.save()
			
			print email_username
			##print list(email_account)
		
		ORM.database_go.close()

smtp_obj = my_smtp(('0.0.0.0', 25), None)

try:
	   asyncore.loop()
except KeyboardInterrupt:
	   pass