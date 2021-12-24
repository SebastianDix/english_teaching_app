#!/usr/bin/env python3
#import backtrace
from flask import Flask, render_template
import trace
import os
from views.lessons import lesson_blueprint
from views.users import user_blueprint
from dotenv import load_dotenv
import ff
load_dotenv()
#from views.feedback import feedback_blueprint
#backtrace.hook(
#reverse=True,
#align=True,
#strip_path=True,
#enable_on_envvar_only=False,
#on_tty=False,
#conservative=False,
#styles={})

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

def getFormFactoryEvents():
    return ff.getAllRelevantEventInfo()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ff')
def formfactory():
    return render_template('formfactory.html', events = getFormFactoryEvents())

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


app.register_blueprint(lesson_blueprint,url_prefix='/lessons')
app.register_blueprint(user_blueprint,url_prefix='/users')
#app.register_blueprint(feedback_blueprint,url_prefix='/feedbacks')

if __name__ == '__main__':
    app.run(debug=True)
