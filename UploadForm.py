from flask_wtf import Form
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Required

class UploadForm(Form):
    '''This is the input form to display'''
    endpoint = StringField('Endpoint:', validators=[Required()])
    access_key = StringField('Access Key', validators=[Required()])
    secret_key = StringField('Secret Key', validators=[Required()])
    bucket_name = StringField('Bucket Name', validators=[Required()])
    file = FileField('File to upload', validators=[Required()])
    submit = SubmitField('Upload')

