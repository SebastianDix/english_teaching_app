#!/usr/bin/python3
import pymongo
from models.analysis import Analysis
import argparse
import smtplib, ssl
import pdfkit
parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

lines = args.file.read().splitlines()

analysis = Analysis("Pavel Kraus","today")
analysis.parseText(lines)
analysis.pdf()

#message = """From: Sebastian Dix <seb@sebdix.eu>
#To: Sebastian Dix <sebastiandix3@gmail.com>
#MIME-Version: 1.0
#Content-type: text/html
#Subject: SMTP HTML e-mail test
#
#This is an e-mail message to be sent in HTML format
#
#<b> This is an HTML message.</b>
#<h1> This is a headline. </h1>
#"""
#context = ssl.create_default_context()
#with smtplib.SMTP('localhost') as server:
    #server.sendmail('seb@lektorpraha.cz','seb@sebdix.eu',message)
