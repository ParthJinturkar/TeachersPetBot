# About !voice_channel

This command lets the user to create voice channels.

# Location of Code

The code that implements the above mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/notification.py).

# Code Description

## Functions

1. voice_channel(self, ctx, channelname: str, catename: str, limit: str, num: str): <br>
   This function takes as arguments the parameters provided by the cuser through self, context in which the command was called, the channel name, category name, max limit of the voice channel, and the number of voice channels. 

# How to run it? (Small Example)

Let's say that you are in the server that has the Classmate Bot active and online. All you have to do is 
enter the command '!voice_channel' pass in all the parameters as a space seperated inputs in the following order:
channel name,  category name, limit, number of channels

```
!addhw CLASSNAME CHA_NAME CATE_NAME D D
!voice_channel teams meeting 10 3
```

Successful execution of this command will create voice channels in the server.

![$voice_channel](https://github.com/qchen59/TeachersPetBot/blob/main/images/gifs/notifications/voice_channel.gif)
