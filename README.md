/r/PuzzleAndDragons scripts
==========================

### Sticky Bot
==============

Simple script that checks if the "fake sticky" post is older than 3 days. If so, creates a new post & updates the fake sticky link to it.


##### Setup

Assumes that you have python and pip (or easyinstall)

```
$ git clone https://github.com/tamadra/r-puzzleanddragons-scripts
$ cd r-puzzleanddragons-scripts
$ pip install praw
```

In sticky-bot.py Replace username/password with your own (but recommended to use the "_moderators" account)

##### Running

```
$ python sticky-bot.py
```

May need to enter a captcha when prompted by reddit.
