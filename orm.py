from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,create_engine,Text
import settings as external_settings

##define the engine to avoid re-reference
engine = create_engine('mysql://%s:%s@%s/%s' % (external_settings.DB_USER,external_settings.DB_PASS,external_settings.DB_HOST,external_settings.DB_NAME))

##keep the table definitions here
metadata = MetaData()

email_account = Table('email_account', metadata,
			Column('id'				, Integer, primary_key=True),
			Column('inbox_name'		, String(60), nullable=False),
			Column('access_key'		, String(60), nullable=False),
		)

emails_recieved = Table('emails_recieved', metadata,
			Column('id'						, Integer, primary_key=True),
			Column('owner_id'				, Integer, ForeignKey("email_account.user_id"), nullable=False),
			Column('email_desc_html'		, Text, nullable=False),
			Column('email_from'				, String(100),nullable=False),
			Column('email_desc_plain'		, Text, nullable=False),
			Column('email_title'			, String(500), nullable=False),
		)