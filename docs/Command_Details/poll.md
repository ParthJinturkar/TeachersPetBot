# About !poll
This command lets the Instructors create a poll with 2 choices. When types the command for poll, 
the bot will delete the command and create the specified poll in the 'general' channel. The command can only be used by the Instructor in the 'instructor-commands' channel.
A listener is also implemented to avoid getting multiple reactions from same member. If the same member does react thumps up and thumps down then the last reaction is discarded.
# Location of Code
The code that implements the above-mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/polling.py)

# Code Description
## Poll Function

poll(self, ctx, *, poll: str = None)

This Function takes in the poll as the argument creates the poll on the 'general' channel. 
It does check where and by whom the command is being used, and will send a error if the !poll command is not used in 'instructor-commands' channel or by Instructor.

## On Reaction Function

on_raw_reaction_add(self, payload)


This Function takes in a reaction as the payload and checks if same member has multiple reacions.
If same member has reacted both thumps up and thumps down then it will discard the last reaction.

# How to run it? (Small Example)
## Poll Function
Let's say that you are the Instructor and in the instructor-commands channel that has the TeachersPet Bot active and online. 
When you type the following command, the command will be deleted and a poll will be created in general channel.
```
!poll poll_content
```

# Example Run
## Poll Function
![!poll](https://github.com/War-Keeper/TeachersPetBot/blob/main/images/gifs/polling/poll.gif)