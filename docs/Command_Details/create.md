# About !create
The create command lets you manually create assignment, exam or ta_office_hours events for the bot. It will first show buttons for the type of event you want to create.
Then you can fill out the details of the event based on the type of event you chose. you can exit out of the event creation process by typing "exit" or "quit".

# Location of Code
The code that implements the above-mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/create.py)

# Code Description
## create_event Function

create_event(self, ctx):

This Function is used to call the event_creation functions. It will first show the user a list of buttons to choose from.
Then it will ask questions that corresponds to the button that the user chose. when it is down, the data will be stored in the database.

# How to run it? (Small Example)
## Create Command
Let's say that you are in the Instructor Commands channel that has the TeachersPet Bot active and online. 
You want to use the create command to create an exam event. So you type the following:
```
!create
```
Then you will see a list of buttons that you can choose from.
```
Exam
Assignment
TA Office Hours
Custom Event
```
You will then be asked questions that corresponds to the button that you chose.
and you can exit out of the event creation process by typing "quit".


# Example Run
## Create Function
![!create](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/createqna/create.gif)
