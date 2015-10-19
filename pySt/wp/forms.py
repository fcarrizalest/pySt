from flask_wtf import Form
from wtforms import SelectField,HiddenField,StringField,PasswordField,SelectMultipleField,widgets
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Wp_Form(Form):
    name = StringField('name', validators=[DataRequired()])


class Wp_grps_Form(Form):
    groups = MultiCheckboxField('Label')


class Wp_tags_Form(Form):
    id_wp = HiddenField('id_wp', validators=[DataRequired()] )
    name = StringField('name', validators=[DataRequired()])


class Wp_Status_Form(Form):
    id_wp = HiddenField('id_wp',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    etype = SelectField(u'type', choices=[ ('task','task'), ('note','note'), ('folder','folder'), ('account','account') ,('client','client') , ('proyect','proyect'),('contact','contact'),('phase','phase')  ])
    nextStatus = StringField('nextStatus', validators=[DataRequired()])

