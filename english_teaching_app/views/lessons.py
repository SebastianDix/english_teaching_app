#!/usr/bin/python3
import json
from datetime import datetime as dt
from flask import Blueprint,render_template,request,url_for,redirect,session,current_app,flash
from models.lesson import Lesson
from models.feedback import Feedback
from models.user import User
from models.user import requires_admin,requires_login
from pprint import pprint,pformat

lesson_blueprint = Blueprint('lessons',__name__)

@lesson_blueprint.route('/')
@requires_login
def index():
    if session.get('email') == current_app.config.get('ADMIN',''):
        lessons = Lesson.all()
    else:
        lessons = Lesson.get_by_student_email(session.get('email'))

    return render_template('lessons/index.html', lessons=sorted(lessons, key = lambda i: i.datetime,reverse=True), now=dt.now())

@lesson_blueprint.route('/new', methods=['GET','POST'])
@requires_admin
def new_lesson():
    if request.method == 'POST':
        student = User.find_by_email(request.form['student']).json_nopassword()

        date = request.form['date']
        time = request.form['time']
        duration = request.form['duration']

        date_time = f'{date} at {time}'
        date_time = dt.strptime(date_time, "%Y-%m-%d at %H:%M")
        topics = request.form['topics']
        feedback = {}

        Lesson(student,feedback,date_time,duration,False,topics).save_to_mongo()

    users = User.all()
    now = dt.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H:%M")
    return render_template('lessons/new_lesson.html',students=users,year=year,month=month,day=day,time=time)

@lesson_blueprint.route('/edit/<string:lesson_id>', methods=['GET','POST'])
@requires_admin
def edit_lesson(lesson_id):
    lesson = Lesson.get_by_id(lesson_id)

    if request.method == 'POST':
        # setting student
        lesson.student = User.find_by_email(request.form['student']).json_nopassword()

        #setting datetime
        date = request.form['date']
        time = request.form['time']
        date_time = f'{date} at {time}'
        lesson.datetime = dt.strptime(date_time, "%Y-%m-%d at %H:%M")

        # setting topics
        lesson.topics = request.form['topics']

        # feedback data is left the same
        lesson.save_to_mongo()
        return redirect(url_for('.index'))

    # if request.method == 'GET'
    date = lesson.datetime.strftime("%Y-%m-%d")
    time = lesson.datetime.strftime("%H:%M")
    students = User.all()
    return render_template('lessons/edit_lesson.html',lesson=lesson, date=date, time=time, students=students)

@lesson_blueprint.route('/edit_feedback/<string:lesson_id>', methods=['GET','POST'])
@requires_admin
def edit_feedback(lesson_id):
    lesson = Lesson.get_by_id(lesson_id)

    if request.method == 'POST':
        write_all = request.form['write_all']
        write_all = request.data
        fb = Feedback([],[],[],[],[])
        fb.parseText(write_all)
        lesson.feedback = fb.json()
        lesson.topics = request.form['topics']
        lesson.save_to_mongo()
        print(request.data)
        return redirect(url_for('.index'))

    fbD = lesson.feedback
    feedback_insert_formatted=''
    for category in fbD:
        for row in fbD[category]:
            feedback_insert_formatted+=f'{row[0]} = {row[1]}\n'
        feedback_insert_formatted+=f'\n'

    feedback_insert_formatted=feedback_insert_formatted.strip()
    headings={
        "vocab":["Vocabulary","Word or phrase","Definition"],
        "mistakes":["Error correction","Mistake","Correction or alternative"],
        "pronunciation":["Pronunciation correction","Pronunciation error","Correction"],
        "grammar":["Grammar","Grammar topic","URL or explanation"],
        "homework":["Homework","Homework title","Assignment or URL"]
    }
    return render_template('lessons/edit_feedback.html',lesson=lesson,items=fbD,feedback=feedback_insert_formatted,headings=headings)


@lesson_blueprint.route('/delete/<string:lesson_id>')
@requires_admin
def delete_lesson(lesson_id):
    Lesson.get_by_id(lesson_id).remove_from_mongo()
    return redirect(url_for('.index'))

@lesson_blueprint.route('/send_feedback/<string:lesson_id>', methods=['GET'])
@requires_admin
def send_feedback(lesson_id):
    lesson = Lesson.get_by_id(lesson_id)
    lesson.pdf()
    return ''

    
@lesson_blueprint.route('/view_feedback/<string:lesson_id>', methods=['GET'])
@requires_login
def view_feedback(lesson_id):
    lesson = Lesson.get_by_id(lesson_id)
    headings={
        "vocab":["Vocabulary","Word or phrase","Definition"],
        "mistakes":["Error correction","Mistake","Correction or alternative"],
        "pronunciation":["Pronunciation correction","Pronunciation error","Correction"],
        "grammar":["Grammar","Grammar topic","URL or explanation"],
        "homework":["Homework","Homework title","Assignment or URL"]
    }
    return render_template('lessons/view_feedback.html',lesson=lesson,items=lesson.feedback,headings=headings)
    return ''

@lesson_blueprint.route('/favorite', methods=['POST'])
@requires_login
def favorite():
    if request.method == 'POST':
        print(request.form['lesson_id'])
        lesson_id = request.form['lesson_id']
        lesson = ""
        if lesson_id:
            try:
                lesson = Lesson.get_by_id(lesson_id)
            except Exception as e:
                print(e)
                return False
        else:
            print("No lesson id has been provided")
            return False

        if lesson.favorite == True:
            lesson.favorite = False
        else:
            lesson.favorite = True
        lesson.save_to_mongo()
    return ''

@lesson_blueprint.route('/sync_feedback', methods=['POST'])
@requires_admin
def sync_feedback():
    if request.method == 'POST':
        # THE ONLY REASON REQUEST USES .DATA IN THIS CASE IS THAT
        # IT USES THE FETCH METHOD, NOT JQUERY AJAX
        data = json.loads(request.data)
        lesson_id = data['lesson_id']
        if lesson_id:
            try:
                lesson = Lesson.get_by_id(lesson_id)
            except Exception as e:
                print(e)
                return 400
        else:
            print("No lessond id has been provided")
            return 400

        write_all = data['text']
        fb = Feedback([],[],[],[],[])
        fb.parseText(write_all)
        lesson.feedback = fb.json()
        lesson.topics = data['topics']
        lesson.save_to_mongo()
        print("Lesson after save")
        print(lesson.json())
        return 'OK', 200

@lesson_blueprint.route('/data', methods=['GET'])
@lesson_blueprint.route('/data/<string:category>', methods=['GET'])
@requires_login
def view_data(category=False):
    if session.get('email') == current_app.config.get('ADMIN',''):
        lessons = Lesson.all()
    else:
        lessons = Lesson.get_by_student_email(session.get('email'))
    # array=[]
    # for lesson in lessons:
    #     feedback = lesson.feedback
    #     vocab = feedback['vocab']
    #     array.append(vocab)
    #     "vocab":["Vocabulary","Word or phrase","Definition"],
    #     "mistakes":["Error correction","Mistake","Correction or alternative"],
    #     "pronunciation":["Pronunciation correction","Pronunciation error","Correction"],
    #     "grammar":["Grammar","Grammar topic","URL or explanation"],
    #     "homework":["Homework","Homework title","Assignment or URL"]
    # }
    return render_template('lessons/view_data.html',lessons=sorted(lessons, key = lambda i: i.datetime,reverse=True))
    # return 'OK', 200
