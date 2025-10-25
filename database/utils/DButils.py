
from utils.bot_logger import setup_logger

class DButils():

    def __init__(self):
        self.templates = self.Query_table
        self.logger = setup_logger()

    def getQueryIdent(self,_qID):
        return self.templates[int(_qID)][0]
    def getExpected(self,_qID):
        return self.templates[int(_qID)][1]
    
    def getQueryStr(self,_qID):
        return self.templates[int(_qID)][2]
    Query_table = {
    1: ("user_insert", 5 ,"""
        INSERT INTO users (username, student_name, affiliation, ss_ranking, personality_traits)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    ""","python3 DatabaseUI.py -s 1 -v blackBolt \"Levinthus Phoenix\" \"Phoenix\" \"3 Stars\" \"Soul Searching\""),
    2: ("event_insert", 2 ,"""
        INSERT INTO events (event_name, event_description)
        VALUES (%s, %s)
        RETURNING id;
    ""","python3 DatabaseUI.py -s 2 -v \"Ghosts on Campus\" \"Has anyone noticed the strange activity in the plaza\""),
    3: ("user_get_all",0, "SELECT * FROM users;","python3 DatabaseUI.py -s 3"),
    4: ("event_get_all",0, "SELECT * FROM events;","python3 DatabaseUI.py -s 4"),
    5: ("user_get_specfic",1, """
        SELECT * FROM users
        WHERE {col} = %s;""","python3 DatabaseUI.py -s 5 -f student_name -v \"Levinthus Phoenix\""),
    6: ("event_get_specfic",1, """
        SELECT * FROM events
        WHERE {col} = %s;""","python3 DatabaseUI.py -s 6 -f event_name -v \"Ghosts on Campus\""),
    7: ("user_update",2,"""
        UPDATE users
        SET {col} = %s WHERE {col2} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 7 -f username student_name -v PhoenixPrince \"Levinthus Phoenix\""),
    8: ("event_update",2,"""
        UPDATE events
        SET {col} = %s WHERE {col2} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 8 -f event_description event_name -v \"HEEEELLLLPP GHOSTS ARE ATTACKING ME\" \"Ghosts on Campus\""),
    9: ("user_delete",1,"""
        DELETE FROM users
        WHERE {col} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 9 -f student_name -v \"Levinthus Phoenix\""),
    10: ("event_delete",1,"""
        DELETE FROM events
        WHERE {col} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 10 -f event_name -v \"Ghosts on Campus\"")
    }
