#!/usr/bin/env python
from requests_html import HTMLSession
from pprint import pprint as pp
from datetime import datetime as dt
import time
import itertools
clubNames=['vrsovicka','vinohradska','eden']

def clubNameToURL(name):
    return "http://"+str(name)+".formfactory.cz/calendar"

def getTodaysEvents(clubName):
    session = HTMLSession()
    r = session.get(clubNameToURL(clubName))
    scheduler = r.html.find('#scheduler',first=True)
    eventRow = scheduler.find('tr')[1]
    today = eventRow.find('td')[dt.weekday(dt.now())]
    events = today.find('.event')
    return events

def getInfoFromEvent(event):
    name = event.find(".event_name",first=True).text
    fromTo = event.find(".eventlength",first=True).text.split('-')
    startTime = time.strptime(fromTo[0],"%H:%M")
    endTime = time.strptime(fromTo[1],"%H:%M")
    room = event.find(".room",first=True).text
    return (name,startTime,endTime,room)

def getInfosFromClub(clubName):
    events = getTodaysEvents(clubName)
    return list(tup + (clubName,) for tup in map(getInfoFromEvent,events))

def getEventsSortedByStart(clubNames):
    eventLists = [getInfosFromClub(club) for club in clubNames]
    combined = list(itertools.chain.from_iterable(eventLists))
    return sorted(combined, key = lambda items: items[1])


def getAllRelevantEventInfo():
    events = [{"name":e[0],"time":time.strftime("%H:%M",e[1]),"location":e[4].capitalize()} for e in getEventsSortedByStart(clubNames)]
    return events

if __name__ == "__main__":
    pp(getAllRelevantEventInfo())
