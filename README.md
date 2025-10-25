# Discord-Bot

Current Idea:

USER <--> Info-Bot <--> Database <--> DB-Interface

- USER: will be able to see posts on forum channels
- Info-bot: will communicate with the database and pull student data and generate posts
- Database: hold student info, 6 Tables: Phoenix, Hufflepuff, Syltherin, Ravenclaw, Gryfindor, and Unaffiliated
- DB-Interface: Series of python scripts to make interacting with the DB trivial

## Enviroment
There are currently 2 `.env` files needed for this to work, obviously api keys and passwords are not hardcoded and being uploaded to the repo. Here are the two files needed to set this up

`./discord-bot/bot.env`
- DISCORD_TOKEN={Discord API token that connects to the bot}
- DISCORD_GUILD={Server name of where the bot currently lives}
- DATABASE_URL={URL the bot uses to talk to the database}
- POSTGRES_USER={DB username that is created upon database init}
- POSTGRES_PASSWORD={DB password that is created upon database init}
- POSTGRES_DB= {DB name that is created upon database init}
- PGADMIN_DEFAULT_EMAIL=admin@example.com
- PGADMIN_DEFAULT_PASSWORD=changeme
- PGADMIN_LISTEN_PORT=5050

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

### DatabaseUI.py
#### How to insert a user
expected values: (username, student_name, affiliation, ss_ranking, personality_traits)
- `python3 DatabaseUI.py -s 1 -v blackBolt "Levinthus Phoenix" "Phoenix" "3 Stars" "Soul Searching"`  

### How to insert an event
expected values: (event_name, event_description)
- `python3 DatabaseUI.py -s 2 -v "Ghosts on Campus" "Has anyone noticed the strange activity in the plaza"`

### How to view all users
- `python3 DatabaseUI.py -s 3`

### How to view all events
- `python3 DatabaseUI.py -s 4`

### How to select a specific user row
pass in the table field and value within that field
- `python3 DatabaseUI.py -s 5 -f student_name -v "Levinthus Phoenix"`

### How to select a specific event row
pass in the table field and value within that field
- `python3 DatabaseUI.py -s 6 -f event_name -v "Ghosts on Campus"`

### How to replace value in a user row
Provide 2 fields and 2 values, the 1st field and value are the change you want, while the 2nd field and value are to identify which row to make the change to
- `python3 DatabaseUI.py -s 7 -f username student_name -v PhoenixPrince "Levinthus Phoenix"`

### How to replace value in a event row
Provide 2 fields and 2 values, the 1st field and value are the change you want, while the 2nd field and value are to identify which row to make the change to
- `python3 DatabaseUI.py -s 8 -f event_description event_name -v "HEEEELLLLPP GHOSTS ARE ATTACKING ME" "Ghosts on Campus"`

### How to delete a user
Provide a field identifier and value 
- `python3 DatabaseUI.py -s 9 -f student_name -v "Levinthus Phoenix"`

### How to delete an event
Provide a field identifier and value 
- `python3 DatabaseUI.py -s 10 -f event_name -v "Ghosts on Campus"`

## TODO-List

- Client terminal to interact with the database
    - ~~python loggers~~
    - ~~pgadmin for debugging~~
    - Implement Json or yaml batch import
    - finish implement basic sql commands
- Connect the bot to interact with the database
    - verify that user has appropriate role for each commands
- Finish setting test entries for database for bot
    - ~~make db schemas~~
    - ~~| id | username | student name | affiliation | SS ranking | post count | personality traits |~~
    - ~~| id | event_id | post_id?| list of people interacting|~~
