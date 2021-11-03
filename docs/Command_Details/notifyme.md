# About !notifyme
This command lets the user display all the homeworks that are due this week for all the courses. 

# Location of Code
The code that implements the above mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/notification.py).

# Code Description
## Functions
1. notify_me(self, ctx, quantity: int, time_unit: str, *, text: str) <br>
This function takes as arguments the values provided by the constructor through self and the context in which the command was called. Then it takes the time value in an integer format and the time unit in the string format. And in the end it takes a string input which is the description of the notification. This command also lets you send the reminder on the channel itself or any text/email.

# How to run it? (Small Example)
Let's say that you are in the server that has the Classmate Bot active and online. All you have to do is 
enter the command '!notifyme' with no other parameters:

```
!notifyme 1 minute Complelete 510 Project 2
```
Successful execution of this command will display all the homeworks that are due this week.

![!notifyme](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/notifications/notifyme.gif)
![!notifyme](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/notifications/notifyme.PNG)
![!notifyme](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/notifications/notifyme2.PNG)
![!notifyme](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/notifications/nm3.jpeg)
![!notifyme](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/notifications/nm4.jpeg)
