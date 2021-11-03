# About !multipoll
This command lets the Instructors create a poll with specified number of choices ( 2 to 10 ). When Instructor types the command for multipoll, 
the bot will delete the command and create the specified poll in the 'general' channel. The command can only be used by the Instructor in the 'instructor-commands' channel.

# Location of Code
The code that implements the above-mentioned gifs functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/polling.py)

# Code Description
## MultiPoll Function

multi_choice(self, ctx, desc: str = None, *choices)

This Function takes in the desc as the argument creates the multipoll with specified choices in the 'general' channel. 
It does check where and by whom the command is being used, and will send a error in DM if the !multipoll command is not used in 'instructor-commands' channel or by Instructor.

# How to run it? (Small Example)
## MultiPoll Function
Let's say that you are the Instructor and in the instructor-commands channel that has the TeachersPet Bot active and online. 
When you type the following command, the command will be deleted and a multipoll will be created in general channel.
```
!multipoll "poll_content" "poll_choice1" "poll_choice2"...
```

# Example Run
## MultiPoll Function
![!multipoll](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/polling/multipoll.gif)