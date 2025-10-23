# Discord-Bot

Current Idea:

USER <--> Info-Bot <--> Database <--> DB-Interface

USER: will be able to see posts on forum channels
Info-bot: will communicate with the database and pull student data and generate posts
Database: hold student info, 6 Tables: Phoenix, Hufflepuff, Syltherin, Ravenclaw, Gryfindor, and Unaffiliated
DB-Interface: Series of python scripts to make interacting with the DB trivial

## Enviroment
There are currently 2 `.env` files needed for this to work, obviously api keys and passwords are not hardcoded and being uploaded to the repo. Here are the two files needed to set this up

`./discord-bot/bot.env`
- DISCORD_TOKEN={Discord API token that connects to the bot}
- DISCORD_GUILD={Server name of where the bot currently lives}
- DATABASE_URL={URL the bot uses to talk to the database}
- POSTGRES_USER={DB username that is created upon database init}
- POSTGRES_PASSWORD={DB password that is created upon database init}
- POSTGRES_DB= {DB name that is created upon database init}

`./database/db.env`
- POSTGRES_USER={DB username that is created upon database init}
- POSTGRES_PASSWORD={DB password that is created upon database init}
- POSTGRES_DB= {DB name that is created upon database init}

## How to run
```
Docker compose up
```
and to stop it
```
Docker compose down
```

## TODO-List

- Client terminal to interact with the database
    - python logger
- Connect the bot to interact with the database
    - verify that user has appropriate role for each commands
- Finish setting test entries for database for bot
    - make db schemas
    - | id | username | student name | house | post count? | personality? |
- Maybe a second DB to track forum posts? 