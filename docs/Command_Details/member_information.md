# About !whois
This command lets the Instructors get information about the member using his/her username. When Instructor types the command for member information, 
the bot will delete the command and display the member information. The command can only be used by the Instructor in the 'instructor-commands' channel.

# Location of Code
The code that implements the above-mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/polling.py)

# Code Description
## MultiPoll Function

get_member_information(self, ctx, *, member_name: str = None)

This Function takes in the member_name as the argument displays the information about member. 
It does check where and by whom the command is being used, and will send a error in DM if the !whois command is not used in 'instructor-commands' channel or by Instructor.

# How to run it? (Small Example)
## Whois Function
Let's say that you are the Instructor and in the instructor-commands channel that has the TeachersPet Bot active and online. 
When you type the following command, the command will be deleted and member information will be displayed.
```
!whois member_username
```

# Example Run
## Whois Function
![!whois](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/member_information/whois.gif)