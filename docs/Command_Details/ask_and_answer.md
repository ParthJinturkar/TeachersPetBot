# About !ask and !answer
This command lets the students and Instructors ask and answer questions in the  a-and-a channel. When you type a question, 
the bot will replace your question with the same question asked by the bot. 
When a student or instructor answers the question the bot will replace their answer with it being written by the bot. 
Both the student answers and Instructor answers will appear separately. Automated Numbering is also enabled so the 
answers will need to have a number in the command in order to specify which question is being addressed.

# Location of Code
The code that implements the above-mentioned gits functionality is located [here](https://github.com/War-Keeper/TeachersPetBot/blob/main/cogs/ask_and_answer.py)

# Code Description
## Ask Function

ask_question(self, ctx, question)

This Function takes in the question as the argument and passes the context and the question to the qna.question method found in the src folder. 
It does check where the command is being used, and will send a error if the !ask command is not asked in the q-and-a channel.

## Answer Function

answer_question(self, ctx, q_num, answer)


This Function takes in a question number and answer as the arguments and passes them to the qna.answer method found in the src folder.
Error checking is also done to make sure the question number is valid and depending on the user, it will determine if the answer is from a Insturctor or a Student.

# How to run it? (Small Example)
## Ask Function
Let's say that you are in the q-and-a channel that has the TeachersPet Bot active and online. 
When you type the following command, the question will be replaced with the same question asked by the bot.
```
!ask "<Must Be in Quotes>"
```

## Answer Function

Let's say that you are in the q-and-a channel that has the TeachersPet Bot active and online. 
When you type the following command, the answer will be replaced with the same answer as the bot.
Depending on the user, the answer will be from a Student or an Instructor.
```
!answer <NUMBER> "<Must Be in Quotes>"
```

# Example Run
## Ask Function
![!ask](https://github.com/War-Keeper/ClassMateBot/blob/main/data/media/group.gif)
## Answer Function
![!answer](https://github.com/War-Keeper/ClassMateBot/blob/main/data/media/group.gif)