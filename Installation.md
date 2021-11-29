# Installation and Testing Guide 
### Create a Discord Bot
To create a Discord Bot, you must:
* have a [Discord Account](https://discord.com/login)
* have a Discord Guild (server) for the bot
* create a Discord bot in the [Developer Portal](https://discord.com/developers/applications), but DO NOT ADD to your server yet ([Follow instructions here](https://realpython.com/how-to-make-a-discord-bot-python/))
* create a `.env` file with your Bot Token and your Guild token and add this to your .gitignore (Discord will automatically regenerate your token if you accidentally upload it to Github)
    ```
    # .env
    DISCORD_TOKEN={your-bot-token}
    GUILD={your-guild-token}
    ```

NOTE: Run the bot before inviting it to your server in order for auto-initiate commands to run

This includes:
* Creating Instructor Role
* Adding server owner to Instructor Role
* Creating Bot channels

### Run Teacher's Pet Bot
To run the Teacher's Pet Bot:
1. Ensure you have the following installed:
    * [Python 3](https://www.python.org/downloads/) 
    * [pip](https://pip.pypa.io/en/stable/installation/)
2. Clone this repo onto your local machine
3. In the repository directory, run `pip install -r requirements.txt`
4. Run `python bot.py` to start the bot
5. Invite the bot to your server ([Follow instructions here](https://realpython.com/how-to-make-a-discord-bot-python/))
    * NOTE:  When using the OAuth2 URL Generator, make sure you check the box which gives your bot Administrative permissions

### Run Tests
Testing is done using the dpytest library, which fakes HTTP requests to simulate user and bot activities. Bot setup is done throught a fixture in conftest.py, which is run automatically when pytest is called. No external bots or other files are needed.
To run tests on the Teacher's Pet Bot:
 1. Tests can be run by running pytest test/test_bot.py through the terminal
 2. If you want to collect coverage, instead run 'coverage run -m pytest test/test_bot.py', then 'coverage report -m' afterwards
For help with testing, read the dpytest API at https://dpytest.readthedocs.io/en/latest/index.html, and/or contact Evan Brown at wevanbrown@gmail.com
