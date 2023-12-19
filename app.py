from ai import ask_ai, delete
from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, SubmitField, FileField
from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

load_dotenv('.env')

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/images')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

file_extension = ['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp']


class AIForm(FlaskForm):
    question = StringField(validators=[InputRequired()])
    photo = FileField(validators=[FileAllowed(file_extension, 'Image only!'),
                                  FileRequired('File was empty!')])
    submit = SubmitField('Upload')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = AIForm()
    if form.validate_on_submit():
        question = form.question.data
        # question = 'what is happening in the image'
        filename = secure_filename(form.photo.data.filename).split('.')[-1]
        amount = len(os.listdir(app.config['UPLOAD_FOLDER']))
        new_filename = f'{amount}.{filename}'
        delete()
        form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        response = ask_ai(question, new_filename)

        return render_template('index.html', form=form, chat=response, image=new_filename)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
