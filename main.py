import datetime
import json
import os
import tkinter as tk
import matplotlib.pyplot as plot
import matplotlib.dates as matdates
import datetime
from spot import Spotify

# https://trello.com/b/jlKH0NwF/homepy


# VARS

records = "records/"

WINDOW_BG2 = '#856ff8'
WINDOW_BG = "#9e90ea"
UI_BG = "#CA6FF8"
TEXT_BG = "#e5b8fc"
CRITICAL_BG = "#ec4ec5"


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
        dir = records
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
            if os.path.isdir(records + index[0]):
                dir = records + index[0] + "/"
                if os.path.isdir(dir + index[1]):
                    dir += index[1] + "/"
                    if os.path.isfile(dir + "".join(index) + ".json"):
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

# Windows as classes

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window config
        self.title("HomePy")
        self.geometry("600x300")
        self['bg'] = WINDOW_BG

        # Frame
        self.mainFrame = tk.Frame(self, bg=WINDOW_BG)

        # Widgets
        self.newDay = tk.Button(self.mainFrame, text="Daily Data", bg=UI_BG, command=InputDay)
        self.loader = tk.Button(self.mainFrame, text="Load data", bg=UI_BG, command=self.loadDays)
        self.ex = tk.Button(self.mainFrame, bg=UI_BG, text="Quit", command=self.destroy)

        # Pack widgets
        self.newDay.pack()
        self.loader.pack()
        self.ex.pack()

        # Pack frame
        self.mainFrame.pack()

        self.mainloop()

    def loadDays(self):
        data = loadData(["2021/5/15", "2021/5/16"])
        DisplayDay(data[0])
        DisplayDay(data[1])

        # Graph showing average completion of dues
        # 1. Break down day objects into an array of arrays of due objs [ [ date, [ dues ] ], [ date, [ dues ] ] ]
        # 2. Translate into array of average completions according to date
        # 3. Graph

        graph_data = [[], []]
        graph_temp = list()
        for item in data:
            graph_temp.append([item['date'], item['dues']])
            tempdate = item['date'].split('/')
            tempdate0 = datetime.datetime(year=int(tempdate[0]), month=int(tempdate[1]), day=int(tempdate[2]))
            graph_data[0].append(tempdate0)

            avg = []
            for due in item['dues']:
                avg.append(due.completion)
            avg_final = sum(avg) / len(avg)

            graph_data[1].append(avg_final)

        plot.plot_date(graph_data[0], graph_data[1], xdate=True)
        plot.gcf().autofmt_xdate()
        plot.show()


class DisplayDay(tk.Tk):
    def __init__(self, day):
        super().__init__()

        # Window config
        self.title(day["date"])

        # Frames
        self.mainFrame = tk.Frame(self)
        self.dueFrame = tk.Frame(self.mainFrame)

        # Widgets
        for due in day["dues"]:
            temp = tk.Frame(self.dueFrame, borderwidth=2, relief=tk.GROOVE)  # kwargs make nice bezel
            tk.Label(temp, text=due.task).pack()
            tk.Label(temp, text=str(due.completion)).pack()
            tk.Label(temp, text=str(due.points)).pack()
            #tk.Label(temp, text=str(due.dueDate)).pack()
            # Lol I forgot I didn't add this yet.

            temp.pack(side="left", padx=3, pady=5)

        self.ex = tk.Button(self.mainFrame, text="Exit", command=self.destroy)


        # Pack widgets
        self.ex.pack(side=tk.BOTTOM)

        # Pack frames
        self.dueFrame.pack(side=tk.TOP)
        self.mainFrame.pack(side=tk.BOTTOM)


class InputDay(tk.Tk):
    def __init__(self):

        super().__init__()
        self.frame = tk.Frame(self, bg=WINDOW_BG)
        self.title("Daily Dues")
        self.sanitizer = list()
        self.create_widgets()
        self.frame.pack()
        self.date = datetime.datetime.now()
        self.config(bg=WINDOW_BG)  # Lesson learned. Layered frames are default BG and non-transparent.
        # Holy shit even the labels are default non-transparent. ttk makes more sense as I go.

        # Data autopopulation:
        #=============================
        # -> Does an entry for this day exist?
        #    -> Yes
        #       -> Populate existing fields accordingly
        #    -> No
        #       -> Generate empty dues
        #          -> Read default due values
        #==============================

        today = datetime.datetime.now()

        if os.path.isfile(
        "records/{year}/{month}/{year}{month}{day}.json".format(
        year = today.year
        month = today.month
        day = today.day)
        ):

    def create_widgets(self):

        dateLabel = tk.Label(master=self.frame, text="Date\n(leave blank for today)", bg=WINDOW_BG)
        dateLabel.pack()

        self.dateEntry = tk.Entry(master=self.frame, bg=TEXT_BG)
        self.dateEntry.pack()  # Made self for sanitization

        dateFormatLabel = tk.Label(master=self.frame, text="(Format: YYYY/MM/DD)", bg=WINDOW_BG)
        dateFormatLabel.pack()

        dueLabel = tk.Label(master=self.frame, text="Dues", bg=WINDOW_BG)
        dueLabel.pack()

        self.duesFrame = tk.Frame(master=self.frame, bg=WINDOW_BG)
        self.duesFrame.pack()

        dueButton = tk.Button(master=self.frame, text="Another Due", command=self.addDue, bg=UI_BG)
        dueButton.pack()

        notesLabel = tk.Label(master=self.frame, text="Notes", bg=WINDOW_BG)
        notesLabel.pack()

        self.notesText = tk.Text(master=self.frame, width=40, height=5, bg=TEXT_BG)
        self.notesText.pack(pady=5, padx=15)

        finButton = tk.Button(master=self.frame, text="Finish", command=self.sanitize, bg=UI_BG)
        finButton.pack()

    #  Creates a structured frame for user input to convert to due obj later
    def addDue(self):
        taskFrame = tk.Frame(master=self.duesFrame, padx=2,  borderwidth=4, relief=tk.GROOVE, bg=WINDOW_BG)
        taskFrame.pack(side="right", padx=4)
        taskFrame.tskFrame = True

        taskLabel = tk.Label(master=taskFrame, text="Task", bg=WINDOW_BG)
        taskLabel.pack(side="top")

        taskEntry = tk.Entry(master=taskFrame, bg=TEXT_BG)
        taskEntry.pack(side="top")

        pointsFrame = tk.Frame(master=taskFrame, bg=WINDOW_BG)
        pointsFrame.pack(side="top")

        pointsLabel = tk.Label(master=pointsFrame, text="Points for due", bg=WINDOW_BG)
        pointsLabel.pack(side="top")

        pointsEntry = tk.Entry(master=pointsFrame, bg=TEXT_BG)
        pointsEntry.pack(side="top")

        completionFrame = tk.Frame(master=taskFrame, bg=WINDOW_BG)
        completionFrame.pack(side="top")

        completionLabel = tk.Label(master=completionFrame, text="Completion value\n(Between 0 and 1)", bg=WINDOW_BG)
        completionLabel.pack(side="top")

        completionEntry = tk.Entry(master=completionFrame, bg=TEXT_BG)
        completionEntry.pack(side="top")

        undoDue = tk.Button(master=taskFrame, text="Remove Due", command = taskFrame.destroy, bg=CRITICAL_BG)
        undoDue.pack()

        self.sanitizer.append([pointsEntry, completionEntry])


    def sanitize(self):

        #  User has declared today's input entered.
        #  Verify the format of all given input
        #  Outcome A: Bad formatting. Prompt user to fix.
        #  Outcome B: Clean formatting. Commit to memory.

        #  Data to sanitize:
        #  Date (YYYY/MM/DD)
        #  Points for due (range of 1-100)
        #  Due completion (Percentage completion in 0f-1f)

        dues = []
        duesOutput = []

        for widge in self.duesFrame.winfo_children():
            if isinstance(widge, tk.Frame) and widge.tskFrame is True:
                dues.append(widge)

        # Date sanitizer
        if self.dateEntry.get() != '':
            try:
                self.date = datetime.datetime.strptime(self.dateEntry.get(), "%Y/%m/%d")
            except ValueError:
                try:
                    self.date = datetime.datetime.strptime(self.dateEntry.get(), "%y/%m/%d")
                except Exception as e:
                    print("You did that wrong! Error handle it!")
                    raise e

        # Due sanitizer
        try:
            for due in dues:
                def _getEntries(widget):
                    if isinstance(widget, tk.Entry):
                        return widget
                    elif isinstance(widget, tk.Frame):  # I used a separate frame to achieve a desired look.
                        for w in widget.winfo_children():  # I did not foresee this headache.
                            if isinstance(w, tk.Entry):
                                return w
                    else:
                        return False
                entries = [_getEntries(w) for w in due.winfo_children() if _getEntries(w)]

                duesOutput.append({
                    "task": entries[0].get(),
                    "points": int(entries[1].get()),
                    "completion": float(entries[2].get())
                })


        except Exception as e:
            print("You did that wrong! Error handle it!")
            raise e

        # To have reached this point indicates clean data, time to ship it off!

        notes = []



        output = Day(
            date=self.date,
            dues=[Due(task=d["task"], completion=d["completion"], points=d["points"]) for d in duesOutput],
            notes=[note for note in self.notesText.get('1.0', tk.END).split('\n')]  # tKinter text isn't 0-based index? It's a string float starting at 1?
        )
        saveData([output])


#temp = Console(tk.Tk())

if __name__ == "__main__":

    temp2 = Root()
    #temp2.mainloop()
