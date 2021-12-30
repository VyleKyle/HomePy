import datetime
import json
import os
import tkinter as tk
import matplotlib.pyplot as plot
import matplotlib.dates as matdates
import datetime
import logging

logging.basicConfig(filename="main.log", encoding="utf-8", filemode='w', level=logging.DEBUG)

# https://trello.com/b/jlKH0NwF/homepy

config = {
    "records": "records/",
    "WINDOW_BG": "#073642",
    "UI_BG": "#586e75",
    "TEXT_BG": "#002b36",
    "CRITICAL_BG": "#835656"
}


# FUNCTIONS


def dayToJSON(day):  # returns dict obj for json use
    if len(day.dues) > 0:
        tempDues = [x.__dict__ for x in day.dues]
    else:
        tempDues = []

    output = day.__dict__.copy()
    output["dues"] = tempDues

    return output


def monthToJSON(month):  # Expect list of Day objects
    output = []
    for day in month:
        output.append(dayToJSON(day))
    return output


def saveData(days):  # Expect list of Day objects
    if not isinstance(days, list):
        raise ValueError(days, "Expected list object")
    for day in days:
        if not isinstance(day, Day):
            raise ValueError(day, "Expected list of Day object.")
        index = day.date.split("/")
        dir = config["records"]
        if os.path.isdir(dir + str(index[0])):  # If year is on record...
            dir += str(index[0] + "/")
            if os.path.isdir(dir + str(index[1])):  # If Month is on record...
                dir += str(index[1] + "/")
                with open(dir + "".join(index) + ".json", "w") as file:
                    file.write(json.dumps(dayToJSON(day)))
            else:  # Month wasn't on record
                os.mkdir(dir + str(index[1]))
                saveData(days)
        else:  # Year wasn't on record?!
            os.mkdir(dir + str(index[0]))
            saveData(days)


def loadData(dates):  # List of string dates in YYYY/MM/DD
    output = []
    if not isinstance(dates, list):
        return ValueError(dates, "Expected list object")
    for day in dates:
        if not isinstance(day, str):
            return ValueError(day, "Expected str containing date")
        try:
            index = day.split("/")  # [year, month, day]
            if len(index) != 3:  # Alright so I think this is what's referred to as spaghetti code.
                return ValueError(day, "Unexpected format, expecting YYYY/MM/DD")
            if os.path.isdir(records + index[0]):  # If year on record...
                dir = records + index[0] + "/"
                if os.path.isdir(dir + index[1]):  # If month on record...
                    dir += index[1] + "/"
                    if os.path.isfile(dir + "".join(index) + ".json"):  #
                        with open(dir + "".join(index) + ".json", "r") as file:
                            tempDay = json.loads(file.read())
                            if len(tempDay["dues"]) > 0:
                                i = 0
                                for due in tempDay["dues"]:
                                    tempDue = Due()
                                    for property in tempDay["dues"][i]:
                                        tempDue.__dict__[property] = tempDay["dues"][i][property]
                                    tempDay["dues"][i] = tempDue
                                    i += 1
                            output.append(tempDay)

        except ValueError as err:
            raise err
    return output


# CLASSES

class Day:

    def __init__(self, date=None, dues=None, notes=None):

        ####
        # Basic information about a given day:
        # date, obj datetime.datetime, expected to contain year/month/day
        # dues, array of obj due
        # notes, array of obj str
        ####

        # DATE LOGIC

        if date is not None and isinstance(date, datetime.datetime):
            self.date = str(date.year) + "/" + str(date.month) + "/" + str(date.day)

        elif date is not None and not isinstance(date, datetime.datetime):
            raise ValueError(date, "Expected datetime object")

        elif date is None:
            today = datetime.datetime.now()
            self.date = str(today.year) + "/" + str(today.month) + "/" + str(today.day)

        # DUES LOGIC

        # Make sure dues a list of dues

        if dues is None or (isinstance(dues, list) and len(dues) < 1):
            self.dues = []

        elif dues is not None and not isinstance(dues, list):
            raise ValueError(dues, "Expected list object")

        else:  # Dues is a list
            for i in dues:
                if isinstance(i, Due):
                    pass
                else:
                    raise ValueError(i, "Expected Due object")
            self.dues = dues

        # NOTES LOGIC

        # Make sure entry is list of strings
        if notes is None:
            self.notes = []
        elif notes is not None and not isinstance(notes, list):
            raise ValueError(notes, "Expected list object")
        else:  # Notes is a list
            for i in notes:
                if not isinstance(i, str):
                    raise ValueError(i, "Expected str object")
            self.notes = notes


class Due:
    ####
    # task, string
    # completion, float, intended range 0-1
    # points, int,
    # dueDate, datetime object
    ####

    def __init__(self, task=None, completion=0.0, points=1, dueDate = None):

        # TASK LOGIC

        # Make sure task is a string
        if task is None:
            self.task = None
        elif not isinstance(task, str):
            raise ValueError(task, "Expected str object")
        else:
            self.task = task

        # COMPLETION LOGIC

        # Make sure completion is a float between 0 and 1
        if (not isinstance(completion, float)) and (not isinstance(completion, int)):
            raise ValueError(completion, "Expected float or int object")
        else:
            if completion < 0 or completion > 1:
                raise ValueError(completion, "Value out of range. Expected between 0 and 1")
            self.completion = completion

        # POINTS LOGIC

        # Make sure points is an int above 0
        if not isinstance(points, int):
            raise ValueError(points, "Expected int object")
        elif points < 1:
            raise ValueError(points, "Value out of range. Expected number above 0")
        else:
            self.points = points

        # DUEDATE LOGIC

        # If duedate, maintain due next day
        # If no duedate, due expires EOD
        if dueDate is None:
            dueDate = datetime.datetime.now().replace(hour=23, minute=59)
        elif not isinstance(dueDate, datetime.datetime):
            print("Error handling due date! Due end of day!")
            pass
