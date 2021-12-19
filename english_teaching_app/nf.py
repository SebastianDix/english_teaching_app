#!/usr/bin/env python
from typing import Dict
import inspect
import socket
from colorama import init as colorama_init
from colorama import Fore,Back
colorama_init(autoreset=True)
# print(Back.LIGHTRED_EX + 'some red text')
from requests_html import AsyncHTMLSession
from pprint import pprint as pp
from datetime import datetime as dt
import time
import itertools
import asyncio
from requests.exceptions import ConnectionError
clubNames=['vrsovicka','vinohradska','eden','karli]
import traceback
import task_logger
import logging

# Possible classes: 
# Club(location, distance, name, types_of_classes_offered,url)
# Event(time,club,name,duration,instructor)

def clubNameToURL(name):
    return "http://"+str(name)+".formfactory.cz/calendar"


def getInfoFromEvent(event):
    name = event.find(".event_name",first=True).text
    fromTo = event.find(".eventlength",first=True).text.split('-')
    startTime = time.strptime(fromTo[0],"%H:%M")
    endTime = time.strptime(fromTo[1],"%H:%M")
    room = event.find(".room",first=True).text
    return (name,startTime,endTime,room)

def getInfosFromClub(clubName,events):
    return list(tup + (clubName,) for tup in map(getInfoFromEvent,events))

def getAllRelevantEventInfo():
    events = [{"name":e[0],"time":time.strftime("%H:%M",e[1]),"location":e[4].capitalize()} for e in getEventsSortedByStart(clubNames)]
    return events

async def _handle_task_result(task: asyncio.Task) -> None:
    try:
        await task
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.
    except Exception:  # pylint: disable=broad-except
        logging.exception('Exception raised by task = %r', task)

async def count(clubName):
    session = AsyncHTMLSession()
    try:
        r = await session.get(clubNameToURL(clubName))
        print(Back.LIGHTBLUE_EX + str(type(r)))
    except ConnectionError as e:
        print(Back.LIGHTRED_EX + "Please check your internet connection" + Back.RESET)
        raise(e)
    except Exception as e:
        raise e

    scheduler = r.html.find('#scheduler',first=True)
    eventRow = scheduler.find('tr')[1]
    today = eventRow.find('td')[dt.weekday(dt.now())]
    events = today.find('.event')
    event_infos = getInfosFromClub(clubName,events)

    return event_infos

async def main():
    event_infos = await asyncio.gather(*list(map(count,clubNames)))
    for i in event_infos:
        if not isinstance(i,ConnectionError) and isinstance(i,Exception):
            raise i
    event_infos = [[] if isinstance(i,Exception) else i for i in event_infos]
    combined = list(itertools.chain.from_iterable(event_infos))
    sorted_infos = sorted(combined, key = lambda items: items[1])
    events = [{"name":e[0],"time":time.strftime("%H:%M",e[1]),"location":e[4].capitalize()} for e in sorted_infos]
    return events 

def get_events() -> Dict:
    main

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    pp(asyncio.run(main()))
    elapsed = time.perf_counter() - s
    print(f"{__file__ if '__file__' in vars(__builtins__) else __name__ } executed in {elapsed:0.2f} seconds.")
