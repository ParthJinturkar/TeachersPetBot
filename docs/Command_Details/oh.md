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
## oh Function
Let's say that you are in the Instructor Commands channel that has the TeachersPet Bot active and online. 
If you want to enter the office hours for the first time, you can use the following command:
```
!oh enter
```
You can then enter an existing group by using the following command:
```
!oh enter <NUMBER>
```
You can then exit the office hours by using the following command:
```
!oh exit
```

# Example Run
## oh Function

##### Entering an office hour (as a student)
Students may wish to receive individual help from a TA or they may want to join other students for help as a group (when they need help with a group project, etc); TeachersPetBot supports both of these use cases. A student may enter the queue as an individual using the `!oh enter` command within the text channel for an ongoing office hour. Upon doing so, a new group will be created and the student will become the sole member of that group. Student may enter existing groups by inputting `!oh enter <group_id>`, where `group_id` is the ID of the group the student wishes to join (group IDs will be displayed in the queue). Once it is an individual's (or group's) turn to be helped by the instructor, all members of the group will be invited into a voice channel where they will be able to talk with the TA.

Upon entering this command in an office hour channel:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_enter.png)

The queue will look like this:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_lone.png)

Upon entering an existing group, say group '000':

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_enter_grp.png)

The queue will look like this:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_group.png)

##### Exiting the office hour queue (as a student)
A student may wish to exit the office hour queue for whatever reason; they may do so by typing `!oh exit` in the channel they are in the queue for.

If a student exists in the queue:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_lone.png)

And enters this command:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_exit.png)

The student will be wiped from the queue:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_empty.png)

##### Traversing the queue (as an instructor)
Once the instructor is ready to help the next student in the queue, they may enter `!oh next` in the office hour text channel. Upon doing so, DMs will be sent to all group members next in the queue notifying them that it is their turn, and they will be able to enter the office hour voice channel.

If a student exists in the queue:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_lone.png)

And an instructor wishes to help the next student in the queue:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_next.png)

The student will be invited to the instructor's voice channel and the queue will be advanced:

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/oh_empty.png)
