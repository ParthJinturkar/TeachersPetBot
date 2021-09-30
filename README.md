# Teacher's Pet <img src="https://github.com/shikhanair/TeachersPetBot/blob/main/images/teacherspet.PNG" alt="alt text" width=75 height=75>

## Streamline Your Class Discord

Software Engineering Project 1 for CSC 510

The Teacher's Pet Bot is a Discord Bot for class instructors to streamline their Discord servers. Discord is a great tool for communication and its functionalities can be enhanced by bots and integrations. There are many tools for organizing classes, but they are often hard to manage. They rarely have good communication mechanisms or ability to connect with other tools. This bot allows instructors to host their classes on Discord, combining communication tools with functionality for assignments, scheduling, and office hours. Instructors and students no longer have to go between platforms to view course details, forums, events, calls, and more.

### Bot Commands


### Installation and Running

#### Tools and Libraries Used
In addition to the packages from [requirements.txt](https://github.com/shikhanair/TeachersPetBot/blob/main/requirements.txt) which need to be installed, please have the following installed on your machine:
* [Python 3.9.7](https://www.python.org/downloads/)
* [Sqlite](https://www.sqlite.org/download.html)

To install and run Teacher's Pet, follow instructions in the [Installation and Testing Guide](https://github.com/shikhanair/TeachersPetBot/blob/main/Installation.md).

### Testing
To run tests on the Teacher's Pet, follow instructions in the [Installation and Testing Guide](https://github.com/shikhanair/TeachersPetBot/blob/main/Installation.md#Run-Tests).

### TeachersPetBot Features

#### Initialization

When Teacher's Pet has been added to a new server as a bot, it will do the following:

* Create a new role called Instructor with Administrative permissions if one does not already exist
* Add the owner of the guild to the Instructor role
* Create a #q-and-a channel if one doesn't already exist
* Create a #calendar channel if one doesn't already exist

In addition to this auto-set up, There is also a command which allows a user with the Instructor role to give the same role to another user. This command will only work for users with the Instructor role already (for example, the guild owner).

#### Q&A
The Q&A functionality allow students to ask and answer questions anonymously. The questions are numbered and when answers are sent, they are combined with the question so they can be easily found. Answers are also marked with `Student Ans` and `Instructor Ans` to distinguish between the sources.  
To ask a question, type `!ask "Question"` in the #q-and-a channel. Example: `!ask "When is the midterm?"`.  
To answer a question type `!answer <question_number> "Answer"` in the #q-and-a channel. Example: `!answer 1 "Oct 12"`.

#### Calendar

#### Office Hours

#### Profanity Censoring

Using the Python package better-profanity, Teacher's Pet will catch profane words sent by members of the guild, delete the message, and re-send the exact message with the bad word(s) censored out. It will also catch profane words in messages which have been edited to incude bad words. This package supports censoring based off any non-alphabetical word dividers and swears with custom characters. NOTE: Currently the Bot does not censor swears which have had extra alphabetical characters added.

### Future Scope
This bot has endless possibilities for functionality. Features which we are interested in adding but did not have time for include but are not limited to:
* Class Polls
* Multi-Guild Handling
* Cloud Hosting
* Detailed Error Handling

For a full list of future features, upgrades, and bug fixes, please visit our [Project 1 Board](https://github.com/shikhanair/TeachersPetBot/projects/1).

### How to Contribute?
Check out our [CONTRIBUTING.md](https://github.com/shikhanair/TeachersPetBot/blob/main/CONTRIBUTING.md) for instructions on contributing to this repo and helping enhance this Discord Bot, as well as our [Code of Conduct](https://github.com/shikhanair/TeachersPetBot/blob/main/CODE_OF_CONDUCT.md) guidelines.

### Team Members
#### Pradhan Chetan
#### Tanya Chu
#### Steve Jones
#### Shikha Nair
#### Alex Snezhko

### License

This project is licensed under the [MIT License](https://github.com/shikhanair/TeachersPetBot/blob/main/LICENSE).
