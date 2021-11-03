# About !eventcsv and !take
The eventcsv command lets instructors get a example CSV of all the events in a course. 
You can download the csv and upload it back to the bot with the take command.
This will let you add all the events to the calendar in one go. 
When using the take command, drag the csv to discord and use the take command in the comment as you upload it.

# Location of Code
The code that implements the above-mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/take.py)

# Code Description
## eventcsv Function

get_event_sample_csv(self, ctx)

This function gets the event sample csvs and returns them as downloadable files.

## take Function

read_exams(self, ctx)

This function lets you save a csv to the bot. It will then add all the events depending on the name of the file to the calendar. 
To use this properly, you should only use this when you are uploading a csv to the bot. and enter the take command in the comment.

# How to run it? (Small Example)
## eventcsv Function
Let's say that you are in the Instructor Commands channel that has the TeachersPet Bot active and online. 
You want to upload a list of events to the bot. You can do this by using the eventcsv command to download the event csvs for assignments and exams and ta_office_hours.
```
!eventcsv
```

## take Function

Let's say that you are in the Instructor Commands channel that has the TeachersPet Bot active and online. 
When you have finished editing the csv, all you have to do is drag it to the discord channel and when it gets to the uploading message, you can use the take command in the comments

```
!take
```

# Example Run
## Ask Function
![!eventcsv](https://github.com/War-Keeper/ClassMateBot/blob/main/data/media/group.gif)
## Answer Function
![!take](https://github.com/War-Keeper/ClassMateBot/blob/main/data/media/group.gif)