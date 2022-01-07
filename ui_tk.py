#!/usr/bin/env python3
import main
import tkinter as tk
import datetime
import os
import logging

logger = logging.getLogger("tkui")
logger.info("Using TK UI")

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window config
        self.title("HomePy")
        self.geometry("600x300")
        self['bg'] = main.config["WINDOW_BG"]

        # Frame
        self.mainFrame = tk.Frame(self, bg=main.config["WINDOW_BG"])

        # Widgets
        self.newDay = tk.Button(self.mainFrame, text="Daily Data", bg=main.config["UI_BG"], command=InputDay)
        self.loader = tk.Button(self.mainFrame, text="Load data", bg=main.config["UI_BG"], command=self.loadDays)
        self.ex = tk.Button(self.mainFrame, bg=main.config["UI_BG"], text="Quit", command=self.destroy)

        # Pack widgets
        self.newDay.pack()
        self.loader.pack()
        self.ex.pack()

        # Pack frame
        self.mainFrame.pack()

        self.mainloop()

    def loadDays(self):
        data = main.loadData(["2021/12/30"])
        DisplayDay(data[0])

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
        self.frame = tk.Frame(self, bg=main.config["WINDOW_BG"])
        self.title("Daily Dues")
        self.sanitizer = list()
        self.date = datetime.date.today()
        self.datestr = self.date.strftime("%Y/%m/%d")
        self.create_widgets()
        self.frame.pack()
        self.config(bg=main.config["WINDOW_BG"])  # Lesson learned. Layered frames are default BG and non-transparent.
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
        main.config["records"] + "{year}/{month}/{year}{month}{day}.json".format(
        year = today.year,
        month = today.month,
        day = today.day)
        ):
            pass
        else:
            print("Yo it came negative dog. I thought I wrote a day...")

    def create_widgets(self):

        dateLabel = tk.Label(master=self.frame, text="Date", bg=main.config["WINDOW_BG"])
        dateLabel.pack()

        self.dateEntry = tk.Entry(master=self.frame, bg=main.config["TEXT_BG"])
        self.dateEntry.insert(0,self.datestr)
        self.dateEntry.pack()  # Made self for sanitization

        dateFormatLabel = tk.Label(master=self.frame, text="(Format: YYYY/MM/DD)", bg=main.config["WINDOW_BG"])
        dateFormatLabel.pack()

        dueLabel = tk.Label(master=self.frame, text="Dues", bg=main.config["WINDOW_BG"])
        dueLabel.pack()

        self.duesFrame = tk.Frame(master=self.frame, bg=main.config["WINDOW_BG"])
        self.duesFrame.pack()

        dueButton = tk.Button(master=self.frame, text="Another Due", command=self.addDue, bg=main.config["UI_BG"])
        dueButton.pack()

        notesLabel = tk.Label(master=self.frame, text="Notes", bg=main.config["WINDOW_BG"])
        notesLabel.pack()

        self.notesText = tk.Text(master=self.frame, width=40, height=5, bg=main.config["TEXT_BG"])
        self.notesText.pack(pady=5, padx=15)

        finButton = tk.Button(master=self.frame, text="Finish", command=self.sanitize, bg=main.config["UI_BG"])
        finButton.pack()

    #  Creates a structured frame for user input to convert to due obj later
    def addDue(self):
        taskFrame = tk.Frame(master=self.duesFrame, padx=2,  borderwidth=4, relief=tk.GROOVE, bg=main.config["WINDOW_BG"])
        taskFrame.pack(side="right", padx=4)
        taskFrame.tskFrame = True

        taskLabel = tk.Label(master=taskFrame, text="Task", bg=main.config["WINDOW_BG"])
        taskLabel.pack(side="top")

        taskEntry = tk.Entry(master=taskFrame, bg=main.config["TEXT_BG"])
        taskEntry.pack(side="top")

        pointsFrame = tk.Frame(master=taskFrame, bg=main.config["WINDOW_BG"])
        pointsFrame.pack(side="top")

        pointsLabel = tk.Label(master=pointsFrame, text="Points for due", bg=main.config["WINDOW_BG"])
        pointsLabel.pack(side="top")

        pointsEntry = tk.Entry(master=pointsFrame, bg=main.config["TEXT_BG"])
        pointsEntry.pack(side="top")

        completionFrame = tk.Frame(master=taskFrame, bg=main.config["WINDOW_BG"])
        completionFrame.pack(side="top")

        completionLabel = tk.Label(master=completionFrame, text="Completion value\n(Between 0 and 1)", bg=main.config["WINDOW_BG"])
        completionLabel.pack(side="top")

        completionEntry = tk.Entry(master=completionFrame, bg=main.config["TEXT_BG"])
        completionEntry.pack(side="top")

        undoDue = tk.Button(master=taskFrame, text="Remove Due", command = taskFrame.destroy, bg=main.config["CRITICAL_BG"])
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
                    logger.exception("Could not parse date")
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
            logger.exception("Error getting tasks")
            raise e

        # To have reached this point indicates clean data, time to ship it off!

        notes = []

        output = main.Day(
            date=self.date,
            dues=[main.Due(task=d["task"], completion=d["completion"], points=d["points"]) for d in duesOutput],
            notes=[note for note in self.notesText.get('1.0', tk.END).split('\n')]  # tKinter text isn't 0-based index? It's a string float starting at 1?
        )
        
        main.saveData([output])

if __name__ == "__main__":
    tmp = Root()
