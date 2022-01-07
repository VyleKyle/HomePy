import datetime
import json
import os
import logging

logging.basicConfig(filename="log", encoding="utf-8", filemode='w', level=logging.DEBUG, datefmt="%m/%d %I:%M:%S", format = "%(asctime)s:%(levelname)s:%(name)s-> %(msg)s")
logger = logging.getLogger("main")
logger.info("-----Main module initialized-----")

# https://trello.com/b/jlKH0NwF/homepy

config = {
    "records": "records/",
    "WINDOW_BG": "#073642",
    "UI_BG": "#586e75",
    "TEXT_BG": "#002b36",
    "CRITICAL_BG": "#835656"
}


# FUNCTIONS


def dayToJSON(day):  # returns internals for json formatting
    if len(day.dues) > 0:
        tempDues = [x.__dict__ for x in day.dues]
    else:
        tempDues = []

    output = day.__dict__.copy()
    output["date"] = day.date.strftime("%Y/%m/%d")
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
        index = day.date.strftime("%Y/%m/%d").split("/")
        dir = config["records"]
        if os.path.isdir(dir + index[0]):  # If year is on record...
            dir += index[0] + "/"
            if os.path.isdir(dir + index[1]):  # If Month is on record...
                dir += index[1] + "/"
                with open(dir + "".join(index) + ".json", "w") as file:
                    file.write(json.dumps(dayToJSON(day)))
            else:  # Month wasn't on record
                os.mkdir(dir + str(index[1]))
                saveData(days)
        else:  # Year wasn't on record?!
            os.mkdir(dir + str(index[0]))
            saveData(days)


def loadData(dates):  # List of string dates in YYYY/MM/DD

    #####
    #
    #       I don't like the way I initially wrote this. I believe it could be
    #       more readable. I still believe in my initial focus in data verification,
    #       however, it should be supplemented with proper comments and whitespace.
    #       This is integral to readable code, reducing mental effort in traversing
    #       and understanding previous work.
    #
    #       Input: List["YYYY/MM/DD"] string formatted dates
    #
    #       Output: List[Day()] objects retrieved from memory based on index date
    #
    #       This is subject to rewriting for potential sql implementation.
    #
    #####

    output = []
    if not isinstance(dates, list):
        raise IndexError(dates, "Expected list object")

    for day in dates:

        if not isinstance(day, str):
            raise IndexError(day, "Expected str containing date")

        try:
            # [year, month, day]
            index = day.split("/")

            if len(index) != 3:
                raise IndexError(day, "Unexpected format, expecting YYYY/MM/DD")

            if os.path.isdir(config["records"] + index[0]):  # If year on record...
                dir = config["records"] + index[0] + "/"

                if os.path.isdir(dir + index[1]):  # If month on record...
                    dir += index[1] + "/"

                    if os.path.isfile(dir + "".join(index) + ".json"):  # If day on record...

                        with open(dir + "".join(index) + ".json", "r") as file:
                            # In hindsight, it might be confusing to index the file by its date,
                            # and simultaneously name it by this elongated, unformatted index.
                            # Although, in a database, I won't be worried with fitting into a filesystem.

                            tempDay = json.loads(file.read())

                            # If there are dues...
                            if len(tempDay["dues"]) > 0:

                                i = 0   # I might reformat this.

                                # Initialize and compile dues

                                # Load each due for given day
                                for due in tempDay["dues"]:

                                    tempDue = Due()

                                    # Load each property for given due
                                    for property in tempDay["dues"][i]:

                                        # Write properties to due
                                        tempDue.__dict__[property] = tempDay["dues"][i][property]

                                    # Write due to day
                                    tempDay["dues"][i] = tempDue
                                    i += 1

                            # Convert str date to datetime
                            tempDay['date'] = datetime.datetime.strptime(tempDay['date'], "%Y/%m/%d")

                            # Initialize Day object and append to output.
                            output.append(Day(date=tempDay["date"], dues=tempDay["dues"], notes=tempDay["notes"]))
                    else:
                        raise ValueError("Day not on record")
                else:
                    raise ValueError("Month not on record")
            else:
                raise ValueError("Year not on record")



        except ValueError as err:
            logger.critical(err)
            raise err
    return output


# CLASSES

class Day:

    def __init__(self, date=None, dues=None, notes=None):

        ####
        # Basic information about a given day:
        # date, str date YYYY/MM/DD
        # dues, array of obj due
        # notes, array of obj str
        ####

        # DATE LOGIC

        if date is not None and isinstance(date, datetime.datetime):
            self.date = date

        elif date is not None and not isinstance(date, datetime.datetime):
            raise ValueError(date, "Expected datetime object")

        elif date is None:
            self.date = datetime.datetime.now()

        # DUES LOGIC

        # Make sure dues is a list of dues

        if dues is None or (isinstance(dues, list) and len(dues) < 1):
            self.dues = []

        elif dues is not None and not isinstance(dues, list):
            raise ValueError(dues, "Expected list object")

        else:  # Verify list is of dues
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

if __name__ == "__main__":
    pass
