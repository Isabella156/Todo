from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, length


# form to collect information of the added assessment
class TodoForm(Form):
    code = StringField('code', validators=[length(max=20), DataRequired()])
    deadline = DateField('deadline', validators=[DataRequired()])
    title = StringField('title', validators=[length(max=100), DataRequired()])
    description = TextAreaField('description', validators=[length(max=500), DataRequired()])
