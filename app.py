#!/usr/bin/python

import os
import tempfile
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from UploadForm import UploadForm
from werkzeug.utils import secure_filename
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import ssl


app = Flask(__name__)  # Instantiate Flask

''' Configure the app.config using the environmental variables otherwise use defaults '''
app.config['PORT'] = os.getenv('PORT', 5000)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ECS is awesome!')
app.config['EXPIRE_TIME'] = os.getenv('EXPIRE_TIME', 300)

Bootstrap = Bootstrap(app)  # Configure bootstrap as static


@app.route('/', methods=['GET', 'POST'])
def root():
    ''' Read the root document and load form'''
    endpoint = 'object.ecstestdrive.com'
    access_key = None
    secret_key = None
    bucket_name = None
    file = None
    form = UploadForm()

    if form.validate_on_submit():  # If form is valid store info in a session
        session['endpoint'] = form.endpoint.data
        session['access_key'] = form.access_key.data
        session['secret_key'] = form.secret_key.data
        session['bucket_name'] = form.bucket_name.data


        url = ecs_upload(bucket_name, form)  # Upload object to ECS
        session['signed_url'] = url
        return redirect(url_for('uploaded'))  # Once file is uploaded redirect to completed page

    return render_template('index.html',
                           form=form,
                           endpoint=session.get(endpoint),
                           access_key=session.get(access_key),
                           secret_key=session.get(secret_key),
                           bucket_name=session.get(bucket_name),
                           file=file)

def ecs_upload(bucket_name, form):
    ''' Upload the file to the ECS storage '''
    filename = secure_filename(form.file.data.filename)  # make sure the filename pass is safe
    conn = S3Connection(aws_access_key_id=session['access_key'],
                        aws_secret_access_key=session['secret_key'],
                        host=session['endpoint']
                       )
    bucket_name = session['bucket_name']
    is_bucket_present = conn.lookup(bucket_name)  # check if there is an exisiting bucket with the same name
    if is_bucket_present is None:  # if there are no buckets, create one
        conn.create_bucket(bucket_name)
    bucket = conn.get_bucket(bucket_name)  # get the bucket
    k = Key(bucket)  # get an object key for it
    k.key = filename
    k.set_contents_from_file(form.file.data)  # store the content in ECS
    expire_time = int(app.config['EXPIRE_TIME'])
    url = conn.generate_url(expires_in=expire_time,
                            method='GET',
                            bucket=bucket_name,
                            key=k.key)
    return url

@app.route('/uploaded', methods=['GET'])
def uploaded():
    ''' Display a page with the link to the uploaded object '''
    sign_url = session['signed_url']
    return render_template('uploaded.html', sign_url=sign_url, expire_at=app.config['EXPIRE_TIME'])

@app.errorhandler(404)
def page_not_found(e):
    ''' Display the page no found message '''
    return render_template('404.html'), 400

@app.errorhandler(500)
def internal_server_error(e):
    ''' Display the server error message '''
    return render_template('500.html'), 500

if __name__ == '__main__':
    #  context=('server.crt', 'server.key')
    app.run(debug=True,
            host='0.0.0.0',
            threaded=True,
            port=int(app.config['PORT']),
            ssl_context='adhoc'  # Use context for customer certs and keys
           )
