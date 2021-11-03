# About !oh
The !oh command is used to control access to office hours for students. It involves using entering, exiting and next 
parameters to notify students and Instructors, so everyone knows whose turn it is. 

# Location of Code
The code that implements the above-mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/oh.py)

# Code Description
## oh Function

office_hour_command(self, ctx, command, *args)

This function is used to handle the !oh command. It takes in the command and arguments, and then calls office_hours file to handle the command parameters.



# How to run it? (Small Example)
## eventcsv Function
Let's say that you are in the Instructor Commands channel that has the TeachersPet Bot active and online. 
If you want to enter the office hours for the first time, you can use the following command:
```
!oh enter
```
This will return the following message:
![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_lone.png)

You can then enter an existing group by using the following command:
```
!oh enter <NUMBER>
```
The queue will be displayed as follows:
![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_group.png)

You can then exit the office hours by using the following command:
```
!oh exit
```
This will return the following message:
![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_empty.png)

