import discord
from discord import Client
from discord.ext import commands
import json
import os
import asyncio
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

from src import logmsg

BOT = None


class Deadline(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reminders = json.load(open("data/remindme/reminders.json"))
        self.notifs = json.load(open("data/remindme/groupremind.json"))
        self.units = {"second": 1, "minute": 60, "hour": 3600, "day": 86400, "week": 604800, "month": 2592000}


    @commands.command(name="addhw",
                      help="add homework and due-date !addhw CLASSNAME HW_NAME MMM DD YYYY optional(HH:MM) ex. !addhw CSC510 HW2 SEP 25 2024 17:02")
    async def duedate(self, ctx, coursename: str, hwcount: str, *, date: str):
        """
        Function:
            duedate(self, ctx, coursename: str, hwcount: str, *, date: str)
        Description:
            Adds the homework to json in the specified format
        Inputs:
            - self: used to access parameters passed to the class through the constructor
            - ctx: used to access the values passed through the current context
            - coursename: name of the course for which homework is to be added
            - hwcount: name of the homework
            - date: due date of the assignment
        Outputs:
            returns either an error stating a reason for failure or returns a success message
          indicating that the reminder has been added
        """
        author = ctx.message.author
        # print('Author: '+str(author)+' coursename: '+coursename+' homework count: '+hwcount+' date: '+str(date))
        try:
            duedate = datetime.strptime(date, '%b %d %Y %H:%M')
            # print(seconds)
        except ValueError:
            try:
                duedate = datetime.strptime(date, '%b %d %Y')
            except:
                await ctx.send("Due date could not be parsed")
                return
        a_timedelta = duedate - datetime.today()
        seconds = (time.time() + a_timedelta.total_seconds())
        flag = True
        if self.reminders:
            for reminder in self.reminders:
                if ((reminder["COURSE"] == coursename) and (reminder["HOMEWORK"] == hwcount)):
                    flag = False
                    break
        if (flag):
            self.reminders.append({"ID": author.id, "COURSE": coursename, "HOMEWORK": hwcount, "DUEDATE": str(duedate),
                                   "FUTURE": seconds})
            json.dump(self.reminders, open("data/remindme/reminders.json", "w"))
            await ctx.send(
                "A date has been added for: {} homework named: {} which is due on: {} by {}.".format(coursename,
                                                                                                     hwcount,
                                                                                                     str(duedate),
                                                                                                     author))
        else:
            await ctx.send("This homework has already been added..!!")
        ###########################
    # Function: create voice channel
    # Description: command to ask question and sends to qna module
    # Inputs:
    #      - ctx: context of the command
    #      - question: question text
    # Outputs:
    #      - User question in new post
    ###########################
    @commands.command(name='voice_channel', help='Create voice channel. Please input channel name, category, limit '
                                                 'and number of channels. ex. !voice_channel teams meeting 10 3')
    async def voice_channel(self, ctx, channelname: str, catename: str, limit: str, num: str):
        ''' Create voice channel command '''
        TESTING_MODE = False
        ''' create voice channel input flow '''
        GUILD = os.getenv("GUILD")
        discord.utils.get(BOT.guilds, name=GUILD)
        # if ctx.channel.name == 'instructor-commands':
        cat_exist = False
        for guild in BOT.guilds:
            # Category
            for cat in guild.categories:
                if cat.name == catename:
                    cat_exist = True
                    print('exist')
                    if int(num) == 1:
                        await guild.create_voice_channel(channelname, user_limit=int(limit), category=cat)
                    else:
                        for i in range(int(num)):
                            temp = channelname + str(i + 1)
                            await guild.create_voice_channel(temp, user_limit=int(limit), category=cat)


        if not cat_exist:
            category = await guild.create_category(catename)
            print('exist')
            if int(num) == 1:
                await guild.create_voice_channel(channelname, user_limit=int(limit), category=category)
            else:
                for i in range(int(num)):
                    temp = channelname + str(i + 1)
                    await guild.create_voice_channel(temp, user_limit=int(limit), category=category)

        await ctx.send("Voice channel has been created!!")

    @duedate.error
    async def duedate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'To use the addhw command, do: !addhw CLASSNAME HW_NAME MMM DD YYYY optional(HH:MM) \n ( For example: !addhw CSC510 HW2 SEP 25 2024 17:02 )')

    @commands.command(name="listreminders", pass_context=True, help="lists all reminders")
    async def listreminders(self, ctx):
        to_remove = []
        for reminder in self.reminders:
            # if reminder["FUTURE"] <= int(time.time()):
            try:
                # await ctx.send("{} homework named: {} which is due on: {} by {}".format(self.bot.get_user(reminder["ID"]), reminder["TEXT"]))
                # await ctx.send("{} homework named: {} which is due on: {} by {}".format(reminder["COURSE"], reminder["HOMEWORK"],reminder["DUEDATE"],self.bot.get_user(reminder["ID"])))
                embed = discord.Embed(colour=discord.Colour.gold(), timestamp=ctx.message.created_at,
                                      title=reminder["COURSE"])
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.add_field(name="Homework Title", value=reminder["HOMEWORK"], inline=False)
                embed.add_field(name="Due Date:", value=reminder["DUEDATE"], inline=False)
                post_author = "<@" + str(reminder["ID"]) + ">"
                embed.add_field(name="Posted By:", value=post_author, inline=False)
                await ctx.send(embed=embed)
            except (discord.errors.Forbidden, discord.errors.NotFound):
                to_remove.append(reminder)
            except discord.errors.HTTPException:
                pass
            else:
                to_remove.append(reminder)
        if not self.reminders:
            await ctx.send("Mission Accomplished..!! You don't have any more dues..!!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send('Unidentified command..please use !help to get the list of available comamnds' + str(error))


    @commands.command(name="deletereminder", pass_context=True,
                      help="delete a specific reminder using course name and homework name using !deletereminder CLASSNAME HW_NAME ex. !deletereminder CSC510 HW2 ")
    async def deleteReminder(self, ctx, courseName: str, hwName: str):
        """
        Function:
            deleteReminder(self, ctx, courseName: str, hwName: str)
        Description:
            Delete a reminder using Classname and Homework name
        Inputs:
            - self: used to access parameters passed to the class through the constructor
            - ctx: used to access the values passed through the current context
            - coursename: name of the course for which homework is to be added
            - hwName: name of the homework
        Outputs:
            returns either an error stating a reason for failure or
         returns a success message indicating that the reminder has been deleted
        """
        author = ctx.message.author
        to_remove = []
        for reminder in self.reminders:
            # print('in json '+str(reminder["HOMEWORK"])+' hwName '+hwName)
            if ((reminder["HOMEWORK"] == hwName) and (reminder["COURSE"] == courseName)):
                # print('true '+hwName)
                to_remove.append(reminder)
                # print('to_remove '+ str(to_remove))
        for reminder in to_remove:
            self.reminders.remove(reminder)
        if to_remove:
            json.dump(self.reminders, open("data/remindme/reminders.json", "w"))
            await ctx.send("Following reminder has been deleted: Course: {}, Homework Name: {}, Due Date: {}".format(
                str(reminder["COURSE"]), str(reminder["HOMEWORK"]), str(reminder["DUEDATE"])))

    @deleteReminder.error
    async def deleteReminder_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'To use the deletereminder command, do: !deletereminder CLASSNAME HW_NAME \n ( For example: !deletereminder CSC510 HW2 )')


    @commands.command(name="changeduedate", pass_context=True,
                      help="update the assignment date. !changeduedate CLASSNAME HW_NAME MMM DD YYYY optional(HH:MM) ex. !changeduedate CSC510 HW2 SEP 25 2024 17:02 ")
    async def changeduedate(self, ctx, classid: str, hwid: str, *, date: str):
        """
        Function:
            changeduedate(self, ctx, classid: str, hwid: str, *, date: str)
        Description:
            Update the 'Due date' for a homework by providing the classname and homewwork name
        Inputs:
            - self: used to access parameters passed to the class through the constructor
            - ctx: used to access the values passed through the current context
            - classid: name of the course for which homework is to be added
            - hwid: name of the homework
            - date: due date of the assignment
        Outputs:
            returns either an error stating a reason for failure or
          returns a success message indicating that the reminder has been updated
        """
        author = ctx.message.author
        flag = False
        try:
            duedate = datetime.strptime(date, '%b %d %Y %H:%M')
        except ValueError:
            try:
                duedate = datetime.strptime(date, '%b %d %Y')
            except:
                await ctx.send("Due date could not be parsed")
                return
        for reminder in self.reminders:
            flag = False
            if ((reminder["HOMEWORK"] == hwid) and (reminder["COURSE"] == classid)):
                reminder["DUEDATE"] = str(duedate)
                a_timedelta = duedate - datetime.today()
                seconds = (time.time() + a_timedelta.total_seconds())
                reminder["FUTURE"] = seconds
                reminder["ID"] = author.id
                flag = True
                if (flag):
                    json.dump(self.reminders, open("data/remindme/reminders.json", "w"))
                    # await ctx.send("{} {} has been updated with following date: {}".format(classid, hwid, reminder["DUEDATE"]))
                    embed = discord.Embed(colour=discord.Colour.blurple(), timestamp=ctx.message.created_at,
                                          title="Updated Courses:")
                    embed.set_footer(text=f"Requested by {ctx.author}")
                    embed.add_field(name="Coursework", value=classid, inline=False)
                    embed.add_field(name="Homework:", value=hwid, inline=False)
                    embed.add_field(name="Due Date:", value=reminder["DUEDATE"], inline=False)
                    await ctx.send(embed=embed)
                    # await ctx.send("Data updated..!!")

    @changeduedate.error
    async def changeduedate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'To use the changeduedate command, do: !changeduedate CLASSNAME HW_NAME MMM DD YYYY optional(HH:MM) \n ( For example: !changeduedate CSC510 HW2 SEP 25 2024 17:02 )')

    # -----------------------------------------------------------------------------------------------------------------
    #    Function:
    #    Description:
    #    Inputs:
    #
    #    Outputs:
    # -----------------------------------------------------------------------------------------------------------------

    @commands.command(name="duethisweek", pass_context=True,
                      help="check all the homeworks that are due this week !duethisweek")
    async def duethisweek(self, ctx):
        """
        Function:
            duethisweek(self, ctx)
        Description:
            Displays all the homeworks that are due this week along with the coursename and due date
        Inputs:
            - self: used to access parameters passed to the class through the constructor
            - ctx: used to access the values passed through the current context
        Outputs:
            returns either an error stating a reason for failure
            or returns a list of all the assignments that are due this week
        """
        time = ctx.message.created_at

        if len(self.reminders) == 0:
            await ctx.send("No dues this week")

        flag = False

        for reminder in self.reminders:
            timeleft = datetime.strptime(reminder["DUEDATE"], '%Y-%m-%d %H:%M:%S') - time
            print("timeleft: " + str(timeleft) + " days left: " + str(timeleft.days))
            if timeleft.days <= 7:
                flag = True
                # await ctx.send("{} {} is due this week at {}".format(reminder["COURSE"], reminder["HOMEWORK"],reminder["DUEDATE"]))
                await ctx.send("Following homeworks are due this week")
                embed = discord.Embed(colour=discord.Colour.blurple(), timestamp=ctx.message.created_at,
                                      title="Due this week")
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.add_field(name="Coursework", value=reminder["COURSE"], inline=False)
                embed.add_field(name="Homework:", value=reminder["HOMEWORK"], inline=False)
                embed.add_field(name="Due Date:", value=reminder["DUEDATE"], inline=False)
                await ctx.send(embed=embed)

        if not flag:
            await ctx.send("No dues this week")


    @commands.command(name="duetoday", pass_context=True, help="check all the homeworks that are due today !duetoday")
    async def duetoday(self, ctx):
        """
        Function:
            duetoday(self, ctx)
        Description:
            Displays all the homeworks that are due today
        Inputs:
            - self: used to access parameters passed to the class through the constructor
            - ctx: used to access the values passed through the current context
        Outputs:
            returns either an error stating a reason for failure or
           returns a list of all the assignments that are due on the day the command is run
        """
        flag = True
        for reminder in self.reminders:
            timedate = datetime.strptime(reminder["DUEDATE"], '%Y-%m-%d %H:%M:%S')
            if timedate.date() == ctx.message.created_at.date():
                flag = False
                # await ctx.send("{} {} is due today at {}".format(reminder["COURSE"], reminder["HOMEWORK"], timedate.time()))
                await ctx.send("Following homeworks are due today")
                embed = discord.Embed(colour=discord.Colour.blurple(), timestamp=ctx.message.created_at,
                                      title="Due this week")
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.add_field(name="Coursework", value=reminder["COURSE"], inline=False)
                embed.add_field(name="Homework:", value=reminder["HOMEWORK"], inline=False)
                embed.add_field(name="Due Date:", value=reminder["DUEDATE"], inline=False)
                await ctx.send(embed=embed)
        if (flag):
            await ctx.send("You have no dues today..!!")

    @commands.command(name="coursedue", pass_context=True,
                      help="check all the homeworks that are due for a specific course !coursedue coursename ex. !coursedue CSC505")
    async def coursedue(self, ctx, courseid: str):
        """
        Function:
            coursedue(self, ctx, courseid: str)
        Description:
            Displays all the homeworks that are due for a specific course
        Inputs:
            - self: used to access parameters passed to the class through the constructor
            - ctx: used to access the values passed through the current context
            - courseid: name of the course for which homework is to be added
        Outputs:
            returns either an error stating a reason for failure or
          a list of assignments that are due for the provided courseid
        """
        course_due = []
        for reminder in self.reminders:
            if reminder["COURSE"] == courseid:
                course_due.append(reminder)
                # await  ctx.send("{} is due at {}".format(reminder["HOMEWORK"], reminder["DUEDATE"]))
                embed = discord.Embed(colour=discord.Colour.blurple(), timestamp=ctx.message.created_at,
                                      title="Due for this course")
                embed.add_field(name="Homework:", value=reminder["HOMEWORK"], inline=False)
                embed.add_field(name="Due Date:", value=reminder["DUEDATE"], inline=False)
                await ctx.send(embed=embed)
        if not course_due:
            await ctx.send("Rejoice..!! You have no pending homeworks for {}..!!".format(courseid))

    @coursedue.error
    async def coursedue_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'To use the coursedue command, do: !coursedue CLASSNAME \n ( For example: !coursedue CSC510 )')

    # ---------------------------------------------------------------------------------
    #    Function:
    #    Description:
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    Outputs:
    # ---------------------------------------------------------------------------------

    @commands.command(name="clearreminders", pass_context=True, help="deletes all reminders")
    async def clearallreminders(self, ctx):
        """
        Function:
            clearallreminders(self, ctx)
        Description:
            Delete all the reminders
        Inputs:
            - self: used to access parameters passed to the class through the constructor
            - ctx: used to access the values passed through the current context
        Outputs:
            returns either an error stating a reason for failure or
             returns a success message stating that reminders have been deleted
        """
        to_remove = []
        for reminder in self.reminders:
            to_remove.append(reminder)
        for reminder in to_remove:
            self.reminders.remove(reminder)
        if to_remove:
            json.dump(self.reminders, open("data/remindme/reminders.json", "w"))
            await ctx.send("All reminders have been cleared..!!")
        else:
            await ctx.send("No reminders to delete..!!")

    @commands.command(name="notifyme", pass_context=True, help="provides a way to set up notifications ex. !notifyme 1 minutes Complete CSC510 Project2")
    async def notify_me(self, ctx, quantity: int, time_unit: str, *, text: str):
        time_unit = time_unit.lower()
        msg_email = ""
        contact = ""
        author = ctx.message.author
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await ctx.send("Invalid unit of time. Select from seconds/minutes/hours/days/weeks/months")
            return
        if quantity < 1:
            await ctx.send("Quantity must not be 0 or negative")
            return
        if len(text) > 1960:
            await ctx.send("Text is too long.")
            return

        seconds = self.units[time_unit] * quantity
        future = int(time.time() + seconds)

        def check(msg):
            # print("inside msg: msg"+msg)
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

        def check_answer(msg):
            # print("inside msg: msg"+msg)
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["email", "text"]

        def check_email(msg):
            # print("inside msg: msg"+msg)
            return msg.author == ctx.author and msg.channel == ctx.channel

        def check_phone(msg):
            # print("inside msg: msg"+msg)
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send("Would you like to receive reminder on your email or phone? [y/n]")
        #logmsg.logerror(ctx.channel.id)
        # print("The id is here" + ctx.channel.id)
        msg = await BOT.wait_for("message", check=check)
        if msg.content.lower() == "y":
            await ctx.send("Great..!! So, [email/text]..??")
            msg_answer = await BOT.wait_for("message", check=check_answer)
            if msg_answer.content.lower() == "email":
                await ctx.send("Enter your email id")
                msg_email_text = await BOT.wait_for("message", check=check_email)
                msg_email = msg_email_text.content.strip()
                await ctx.send("I will remind you through mail")
            elif msg_answer.content.lower() == "text":
                await ctx.send("Enter your contact number")
                msg_contact = await BOT.wait_for("message", check=check_phone)
                contact = msg_contact.content.strip()
                await ctx.send("I will remind you through text")

        self.notifs.append({"ID": author.id, "FUTURE": future, "TEXT": text, "EMAIL": msg_email, "PHONE": contact, "GUILD": ctx.channel.id})

        await ctx.send("I will remind you that in {} {}.".format(str(quantity), time_unit + s))
        json.dump(self.notifs, open("data/remindme/groupremind.json", "w"))

    async def notification_reminders(self):
        print("inside delete old notifications")
        while self is self.bot.get_cog("Deadline"):
            to_remove = []
            for notif in self.notifs:
                if notif["FUTURE"] <= int(time.time()):
                    try:
                        # await ctx.send("A reminder has been deleted")
                        await self.bot.wait_until_ready()
                        channel = self.bot.get_channel(notif["GUILD"]);
                        await channel.send(
                            "<@{}>, You asked me to remind you this: {}".format(notif["ID"], notif["TEXT"]))
                        if notif["EMAIL"]:
                            await self.email_alert("You have a reminder, Sir",
                                                   "You asked me to remind you this: {}".format(notif["TEXT"]),
                                                   notif["EMAIL"])
                        if notif["PHONE"]:
                            await self.phone_alert("You have a reminder, Sir",
                                                   "You asked me to remind you this: {}".format(notif["TEXT"]),
                                                   notif["PHONE"])
                        print("Deleting an old notification..!!")
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(notif)
                    except discord.errors.HTTPException:
                        pass
                    # except AttributeError as e:
                    #     logerror.logerror(str(e), logerror.get_today())
                    else:
                        to_remove.append(notif)
            for notif in to_remove:
                self.notifs.remove(notif)
            if to_remove:
                json.dump(self.notifs, open("data/remindme/groupremind.json", "w"))
            await asyncio.sleep(5)

    async def email_alert(self, subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        user = "teacher.petbot@gmail.com"
        msg['from'] = user
        password = "bbyfvjamujjjwrna"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

        server.quit()

    async def phone_alert(self, subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to + "@tmomail.net"
        user = "teacher.petbot@gmail.com"
        msg['from'] = user
        password = "bbyfvjamujjjwrna"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

        server.quit()

    async def delete_old_reminders(self):
        """
        Function:
            delete_old_reminders(self)
        Description:
            asynchronously keeps on tracking the json file for expired reminders and cleans them.
        Inputs:
            - self: used to access parameters passed to the class through the constructor
        Outputs:
            deletes the expired reminders and sends a message
        """
        print("inside delete old reminders")
        while self is self.bot.get_cog("Deadline"):
            to_remove = []
            for reminder in self.reminders:
                if reminder["FUTURE"] <= int(time.time()):
                    try:
                        # await ctx.send("A reminder has been deleted")
                        channel = self.bot.get_channel(897661152371290172);
                        await channel.send(
                            "The due date for {} {} which was {} set by <@{}> has now passed".format(reminder["COURSE"],
                                                                                                     reminder[
                                                                                                         "HOMEWORK"],
                                                                                                     reminder[
                                                                                                         "DUEDATE"],
                                                                                                     reminder["ID"]))
                        print("Deleting an old reminder..!!")
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(reminder)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(reminder)
            for reminder in to_remove:
                self.reminders.remove(reminder)
            if to_remove:
                json.dump(self.reminders, open("data/remindme/reminders.json", "w"))
            await asyncio.sleep(5)


# -----------------------------------------------------------------------------
# checks if the folder that is going to hold json exists else creates a new one
# -----------------------------------------------------------------------------
def check_folders():
    if not os.path.exists("data/remindme"):
        print("Creating data/remindme folder...")
        os.makedirs("data/remindme")


# ----------------------------------------------------
# checks if a json file exists else creates a new one
# ----------------------------------------------------
def check_files():
    f = "data/remindme/reminders.json"
    group = "data/remindme/groupremind.json"

    print("Creating file...")
    if not os.path.exists(f):
        print("Creating empty reminders.json...")
        json.dump([], open(f, "w"))

    if not os.path.exists(group):
        print("Creating group reminders file")
        json.dump([], open(group, "w"))


# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
def setup(bot):
    check_folders()
    check_files()
    n = Deadline(bot)
    loop = asyncio.get_event_loop()
    loop_notify = asyncio.get_event_loop()
    loop.create_task(n.delete_old_reminders())
    loop_notify.create_task(n.notification_reminders())
    global BOT
    BOT = bot
    bot.add_cog(n)
