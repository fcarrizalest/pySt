from flask_wtf import Form
from wtforms import StringField,PasswordField,SelectMultipleField,widgets
from wtforms.validators import DataRequired


class MultiCheckboxField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()


class User_Form(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	groups = MultiCheckboxField('Label')


class Group_Form(Form):
	name = StringField('name', validators=[DataRequired()])

