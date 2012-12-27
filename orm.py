from peewee import *
import peewee

import settings as external_settings

database_go 	= peewee.MySQLDatabase(external_settings.DB_NAME,
										host	=	external_settings.DB_HOST,
										user	=	external_settings.DB_USER,
										passwd	=	external_settings.DB_PASS
									)
									
class email_account(peewee.Model):
	class Meta:
		database = database_go

	inbox_name			= CharField()
	access_key			= CharField()


class emails_recieved(peewee.Model):
	class Meta:
		database = database_go

	email_title			= CharField()
	email_desc			= TextField()
	owner				= ForeignKeyField(email_account)
	email_from			= CharField()