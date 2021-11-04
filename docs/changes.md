
The following changes have been made to TeachersPetBot
==========================================================
- Automatic style checking through **Pylint** has been enabled on files. **Pylint** was previously only running on an empty src directory, leading to no actual style coverage.
- Commands have been separated into individual files, making the project more organized and easier to read. 
- Commands have been reformated to use the **Cogs** system, which increases modularity and ease of development. **Cogs** are simpler, more organized, easier to develop versions of regular discord commands that also allow us to use the dpytest testing library for automated testing.
- As a result of the above changes individual commands no longer have any interaction or dependencies on each other, making debugging significantly easier and significantly speeding up development.
- The previous version of this project implemented testing via a separate testing bot, which requires both bots be active and a command to be manually run to initiate testing. This made automatic on-push testing impossible, as the bot and its tester needed to be physically present on a server when testing commenced. The test suite has been completely revamped to use **dpytest**, an automatic testing suite which uses fake HTTP requests to simulate the bot and users on a virtual server. This allows us to automatically test on-push, and also generate and upload coverage reports to codecov.
- Reminders have been added through notification.py, allowing discord, email, and even phone alerts for assignments.
- CSV reading to create events has been added allowing for automatic updating of a course calendar
- The setInstructor command now properly gives the instructor role to the provided user, instead of giving the role to the user who called the command
- Information about each member in the server can now be retrieved through the member info command
- Opinion polling has been added through polling.py, supporting multiple choice commands to quickly gather user feedback.
- 14 new commands have been added, bringing the total up from 8 to 22.
- Descriptions and documentation have been added for each command, providing clear tutorials for bot functionality. Previously there was no individual documentation for each command, previously all commands were documented together.
- Demonstration GIFs have been added for each command, which should provide clear examples for the expected output of each command.
- Voice channels are now automatically created on-run for each project group in the class, which should provide hangout spots for groups to discuss development.
- Errors in event creation through !create has been fixed, it now properly waits for user input before moving to the next phase of event creation, allowing Exams, Assignments, and Office hours to be correctly scheduled.
- Multiple source files have been updated to remove minor bugs, syntax errors, and clean up formatting.
