from flask_wtf import Form
from wtforms import IntegerField,TextAreaField,HiddenField,SelectField,StringField,PasswordField,SelectMultipleField,widgets
from wtforms.validators import Length,DataRequired,Email
from wtforms.fields.html5 import DateTimeField,EmailField,URLField


class Searh_Form(Form):

	wps = SelectField( u'Wps' )
	tags = SelectField(u'Tags' )
	type = SelectField(u'type', choices=[ ('all','all'),('client','client') , ('proyect','proyect')  ])
	q = StringField()


class New_Entity_Form():
	id = HiddenField(u'id')
	name = StringField(u'name',validators=[DataRequired(),Length(min=3)])
	id_wp = HiddenField(u'id_wp', validators=[DataRequired()])
	status = SelectField( u'Status' )
	etype =  HiddenField(u'etype',validators=[DataRequired()])


class New_Account_Form(Form,New_Entity_Form):
	account_type = SelectField(u'type', choices=[ ('repository','repository'),('database','database') , ('ftp','ftp'), ('control_panel','control_panel')   ])
	path = StringField(u'path')
	user = StringField(u'user')
	password =  PasswordField( u'password') 
	host = StringField(u'host') 
	base_datos = StringField(u'user')
	port = IntegerField( u'port')


class New_Task_Form(Form,New_Entity_Form):
	date_start = DateTimeField('date_start')
	date_end = DateTimeField('date_end')


class New_Proyect_Form(Form,New_Entity_Form):
	#type Repositorios,
	pass


class New_Folder_Form(Form,New_Entity_Form):
	pass


class New_Phase_Form(Form,New_Entity_Form):
	phase 	= IntegerField('phase')
	type = SelectField('type', choices=[('web','web'),('desktop','desktop'),('movil','movil')])
	owner = StringField(u'owner')
	planned_date_start = DateTimeField('planned_date_start')
	planned_date_end = DateTimeField('planned_date_end')
	real_date_start = DateTimeField('real_date_start')
	real_date_end = DateTimeField('real_date_end')
	name_proyect = StringField(u'name_proyect')
	tags = StringField(u'tags')
	snippet = StringField(u'snippet')
	goals = StringField(u'goals')
	budget = StringField(u'budget')
	

class New_Note_Form(Form,New_Entity_Form):
	
	#Extra fields
	note =  TextAreaField()


class New_Contact_Form(Form,New_Entity_Form):
	email = EmailField(u'email', validators=[Email()])
	phone = StringField(u'phone')
	position = StringField(u'position')


class New_Client_Form(Form,New_Entity_Form):

	#Extra fields
	first_name = StringField(u'first_name', validators=[DataRequired()])
	last_name = StringField(u'last_name')
	address = TextAreaField(u'address')
	phone = StringField(u'phone')
	email = EmailField(u'email', validators=[Email()])
	site = URLField(u'site')
