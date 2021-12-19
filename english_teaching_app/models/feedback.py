#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
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
import uuid
import json
import re
from models.model import Model
from models.lesson import Lesson
from typing import Dict,List
from dataclasses import dataclass,field

jinja = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@dataclass
class Feedback(Model):
    collection: str = field(init=False, default="feedbacks")
    vocab:List
    mistakes:List
    pronunciation:List
    grammar:List
    homework:List
    _id:str = field(default_factory = lambda: uuid.uuid4().hex)



    def json(self):
        return {
            'vocab':self.vocab,
            'mistakes':self.mistakes,
            'pronunciation':self.pronunciation,
            'grammar':self.grammar,
            'homework':self.homework
        }

    def parseText(self,Lines:str):
        print(Lines)
        print("nuf")
        count = 0
        target = 0
        order = ["vocab","mistakes","pronunciation","grammar","homework"]

        for line in Lines.splitlines():
            count = count + 1
            both = line.strip().split(" = ")
            if len(both) == 1 and both[0] == "":
                if count == 1:
                    pass
                if count != 1:
                    target = target + 1

            if len(both) == 2:
                current = getattr(self,order[target])
                current.append([both[0],both[1]])
                setattr(self,order[target],current)

    def html(self):
        items = self.json()
        vocab = self.vocab
        mistakes = self.mistakes
        pronunciation = self.pronunciation
        grammar = self.grammar
        homework = self.homework

        temp = jinja.get_template("feedbacks/pdf.html").render(
            vocab=vocab,mistakes=mistakes,pronunciation=pronunciation,grammar=grammar,homework=homework,items=items)
        return temp

