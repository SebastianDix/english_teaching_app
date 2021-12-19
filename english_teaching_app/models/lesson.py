#!/usr/bin/env python3
import uuid
import json
import re
from models.model import Model
from typing import Dict
from dataclasses import dataclass,field
from datetime import datetime as dt
from datetime import timedelta
from common.database import Database
import pdfkit
import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename
from premailer import transform
from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


@dataclass
class Lesson(Model):
    collection: str = field(init=False, default="lessons")
    student:Dict
    feedback:Dict
    datetime:str
    duration:int
    favorite:bool
    topics:str = field(default="")
    _id:str = field(default_factory = lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id":self._id,
            "student":self.student,
            "feedback":self.feedback,
            "datetime":self.datetime,
            "topics":self.topics,
            "duration":self.duration,
            "favorite":self.favorite
        }

    def get_how_long_ago(self):
        diff = dt.now() - self.datetime
        seconds = int( diff.seconds)
        minutes = int( seconds / 60)
        hours = int( minutes / 60)
        days = int( hours / 24)
        weeks = int( days / 7)
        months = int(weeks / 4)
        years = (months / 12)

        if years != 0:
            return f'{years} year(s)'
        if months != 0:
            return f'{months} month(s)'
        if weeks != 0:
            return f'{weeks} week(s)'
        if days != 0:
            return f'{days} day(s)'
        if hours != 0:
            return f'{hours} hour(s)'
        if minutes != 0:
            return f'{minutes} minute(s)'
        if seconds != 0:
            return f'{seconds} second(s)'

        return {
            "seconds" : seconds,
            "hours" : hours,
            "minutes" : minutes,
            "hours" : hours,
            "days" : days,
            "weeks" : weeks
        }

    @classmethod
    def get_by_student_email(cls,student_email: str) -> "Lesson":
        return cls.find_many_by("student.email",student_email)

    @classmethod
    def get_by_date(cls,date: str) -> "Lesson":
        url_regex = {"$regex":"^{}".format(date)}
        return cls.find_one_by("date", url_regex)

    @classmethod
    def find_by_url(cls,url:str) -> "Lesson":
        """
        return a lesson from a url like "https://www.alza.cz/item/sdjfksdlfkjfd.html"
        :param url: The item's URL
        :return: a Lesson
        """
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        date = match.group(1)
        return cls.get_by_date(date)

    def pdf(self):
        print("PDF in models lesson being called")
        s = self.student
        first=s['firstname']
        last=s['lastname']
        #{self.datetime.strftime("%Y_%m_%D_%H_%M")}
        pdfname=f'/tmp/{first}{last}.pdf'
        print(pdfname)
        fb = self.feedback
        items = self.feedback

        headings={
            "vocab":["Vocabulary","Word or phrase","Definition"],
            "mistakes":["Error correction","Mistake","Correction or alternative"],
            "pronunciation":["Pronunciation correction","Pronunciation error","Correction"],
            "grammar":["Grammar","Grammar topic","URL or explanation"],
            "homework":["Homework","Homework title","Assignment or URL"]
        }

        print("BEFORE RENDER TEMPLATE")
        temp = jinja.get_template("feedbacks/pdf.html").render(items=items,headings=headings)
        #temp = render_template('web.html',items=items)
        print("AFTER RENDER TEMPLATE")
        #print(temp)

        msg = MIMEMultipart('alternative')
        #from {self.date}, {self.time}
        print(self.datetime)
        date = self.datetime.strftime('%Y-%m-%d') 
        msg['Subject'] = f'{date} English Lesson Feedback for {first} {last}'
        msg['From'] = 'seb@sebdix.eu'
        msg['To'] = self.student['email']
        msg['Cc'] = 'sebastiandix3@gmail.com'       # Here we use the MIME classes to generate headers and content
        # the "transform" function is from a thing called "premailer" which is a way to
        # conver styles defined in <style> tag into inline html elements
        # cuz html email is best supported using inline stuff
        text = "This is the plain version of this email." #TODO delete this
        part1 = MIMEText(text,'plain')
        part2 = MIMEText(transform(temp),'html') #.add_header("Content-Type","text/html")
        msg.attach(part1)
        msg.attach(part2)

        options={'page-size': 'A4',
                 'margin-top': '0.75in',
                 'margin-right': '0.75in',
                 'margin-bottom': '0.75in',
                 'margin-left': '0.75in',
                 'encoding': "UTF-8",
                 'minimum-font-size':'18'}
        print("BEFORE PDFKIT")
        pdfkit.from_string(transform(temp),pdfname,options=options)
        print("AFTERPDFKIT")
        with open(pdfname,"rb") as f:
            attach = MIMEBase('application','pdf')
            attach.set_payload(f.read())
            encoders.encode_base64(attach)
            #attach = MIMEApplication(f.read(),_subtype="pdf")
            attach.add_header('Content-Disposition','attachment',filename=f'{date} English Lesson Feedback for {first} {last}.pdf')
            msg.attach(attach)

            context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            with smtplib.SMTP('localhost') as server:
                server.starttls(keyfile='/etc/letsencrypt/live/sebdix.eu/privkey.pem',certfile='/etc/letsencrypt/live/sebdix.eu/fullchain.pem')
                server.send_message(msg)
                server.quit()
