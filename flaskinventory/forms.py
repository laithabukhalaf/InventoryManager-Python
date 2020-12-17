from flask_wtf import FlaskForm
# The WTF is a built-in module of the flask
#  which provides an alternative way of designing
#  forms in the flask web applications.
from wtforms import StringField,IntegerField,SelectField,SubmitField
from wtforms.validators import DataRequired,NumberRange



class addproduct(FlaskForm):
    prodname = StringField('Product Name', validators=[DataRequired()])
    prodsubmit = SubmitField('Save Changes')

class editproduct(FlaskForm):
    editname = StringField('Product Name', validators=[DataRequired()])
    editsubmit = SubmitField('Save Changes')

class addlocation(FlaskForm):
    locname = StringField('Location Name', validators=[DataRequired()])
    locsubmit = SubmitField('Save Changes')

class editlocation(FlaskForm):
    editlocname = StringField('Location Name', validators=[DataRequired()])
    editlocsubmit = SubmitField('Save Changes')

class moveproduct(FlaskForm):
    mprodname = SelectField(
        'Product Name')
    src = SelectField(
        'Source')
    destination = SelectField(
        'Destination')
    mprodqty = IntegerField('Quantity', validators=[NumberRange(min=5, max=1000000),DataRequired()])
    movesubmit = SubmitField('Move')
