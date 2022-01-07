HomePy
=======
---
###### _by Kadien_
###### [_[Trello board]_](https://trello.com/b/jlKH0NwF/homepy)

A project for the purpose of advancing my own knowledge through challenge.

Features being worked on:

- UI
- CLI functionality

Planned features:

- Cryptocurrency and financial monitoring
- Spotify manipulation through web API calls

---
Dev log:

I like this new logging setup. I think it's primitive compared to what's possible, perhaps a challenge would be to maintain a 'recent' log, and on every start, move that log to a generic log folder, renamed according to the formatted datetime on the first line.

I've relabeled recurring dues as CLI functionality, I'd like to use crontab to automate enacting certain functions on a timely basis. Examples include checking dues against duedates to mark for expiration, spotify client authentication, and spotify playhead management.

I've gone through main.loadData and made it much more visually acceptable. It wasn't serving its predefined output, which was a list of initialized day objects. It does that now. Loading data in the TK UI is broken now, it's been noted in trello, I'll cross that bridge when I care about it again. For now, I'm focusing on the QT implementation.

Once I have the QT implementation up to speed with what I've done with TK, I'd like to investigate sql and database usage, and how it could potentially relate to my current storage of information. I'll start by leveraging alleged sql support offered by QT, and hopefully it's somehow accessible to the TK interface.

I've found a bug trying to use the save functionality. In my debugging, I've found the issue to be the Day class was converting the datetime obj to a poorly formatted string.

I took too long to push a commit and now I have daily data nearly finished in qt. Perhaps I'm undervaluing the experience of building what I have in TK, however, I'm believing QT has been a better experience thus far. Attempting to maintain them simultaneously will ultimately test which one is more preferable.
