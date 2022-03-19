# A simple Discord Ticket Bot

## What is this?

- This is a discord ticketing bot built using python and the nextcord api.
- To setup the bot, go in the configuration.json file and put in all the respective IDs and tokens.
- If you do not want ticket transcripts, then leave TRANSCRIPT_CHANNEL_ID as 0.
- The categories correspond to what categories the person opening a ticket can choose from, a description is required as it will be shown in the dropdown menu along with the category name.
- If you encounter any issues with the bot not working / the code breaking in certain cases feel free to contact me on discord or on my contact email.
- If you want custom bots made for your own server then you can contact me on discord or on my contact email, please note that the work is NOT free.

<br>

---
<br>

## How does it work?

- The bot only has one command, which is menu, prefixed by whatever prefix you choose in the configuration file.
- Using the command pops up a menu from where the user can open a ticket using a button, once the user clicks the button a channel is made with their name and a dropdown with the 3 categories and their descriptions is shown.
- Once the user chooses a category, the channel is renamed to "{category}-{user name}" and a message is displayed there explaining everything for the user and the staff team.
- The message displayed has a button for closing the ticket, once pressed it will begin a 5 second timer and the channel will be deleted, followed by a transcript being sent to the transcripts channel if the ID is given in the configuration file
- Only people with administration permissions in your server, people who have the role with the TICKET_ROLE id and the person who opened the ticket can view the ticket or send messages in it.
- If the bot is restarted, you must run the menu command again to refresh the menu and its buttons. (I am actively looking for a possible workaround for this)

<br>

---

<br>

## Please help I am confused!?

- In case you are stuck on something or do not know how something works in this bot, I think this link might be best for you to find a solution - https://google.com 
- I wish you good luck!

<br>

---

<l align="center">
<footer>
  <h4>Discord - WonkyPigs#0001</h4>
  <h4>Contact Email - contact@wonkypigs.dev</h4>
</footer>
</l>
