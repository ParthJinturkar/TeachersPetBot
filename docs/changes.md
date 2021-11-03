### File highlighting the changes made to the previous version of the project.

We have made the following changes in the previous version:

- Automatic style checking through pylint has been enabled on files. Pylint was previously only running on an empty src directory, leading to no actual style coverage.
- Commands have been separated into individual files, making the project more organized and easier to read. 
- Commands have been reformated to use the cogs system, which increases modularity and ease of development. Cogs are simpler, more organized, easier to develop versions of regular discord commands that also allow us to use the dpytest testing library for automated testing.
- As a result of the above changes individual commands no longer have any interaction or dependencies on each other, making debugging significantly easier and significantly speeding up development.
- The previous version of this project implemented testing via a separate testing bot, which requires both bots be active and a command to be manually run to initiate testing. This made automatic on-push testing impossible, as the bot and its tester needed to be physically present on a server when testing commenced. The test suite has been completely revamped to use dpytest, an automatic testing suite which uses fake HTTP requests to simulate the bot and users on a virtual server. This allows us to automatically test on-push, and also generate and upload coverage reports to codecov.
- Multiple source files have been updated to remove bugs and clean up formatting.
- We implemented a newer method of handling code in this project as the previous one had some problems and did not provide us with the required results.
- We have corrected the context of the project as it was working on a wrong one previously.
- We have enhanced the previously present functionalities like "create" or "answer" and have also added new functionalities like "notification reminder" and "polling" feature.
- We have given individual pages to the description of all the commands (old and new) so that it becomes easier for the user.
- We have added GIFs of the commands so that user can see hoe to correctly use the commands.
