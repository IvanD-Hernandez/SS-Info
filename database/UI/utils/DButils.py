import json
from utils.bot_logger import setup_logger
from pathlib import Path

class DButils():

    def __init__(self):
        self.templates = self.Query_table
        self.logger = setup_logger()
        self.defJson = Path(__file__).parent / "json"
        self.defNum = 10

    def genUserTemplate(self):
        tempList = []
        for _ in range(self.defNum):
            tempList.append(self.userTemplate.copy())
        
        _ret = {}
        _ret["1"] = tempList

        self.writeJson(self.defJson/"userTemplate.json",_ret)
    
    def genEventTemplate(self):
        tempList = []
        for _ in range(self.defNum):
            tempList.append(self.eventTemplate.copy())
        
        _ret = {}
        _ret["2"] = tempList

        self.writeJson(self.defJson/"eventTemplate.json",_ret)


    def readJson(self,filePath):
        with open(filePath, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def writeJson(self,filePath,data):
        with open(filePath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def getQueryIdent(self,_qID):
        return self.templates[int(_qID)][0]
    
    def getExpected(self,_qID):
        return self.templates[int(_qID)][1]
    
    def getQueryStr(self,_qID):
        return self.templates[int(_qID)][2]
    
    def getInsertValues(self,data):
        uName = data["username"]
        sName = data["student_name"]
        affil = data["affiliation"]
        ssRank = data["ss_ranking"]
        ptStr = "{" + data["personality_traits"] + "}"
        return tuple([uName,sName,affil,ssRank,ptStr])
    
    def getInsertEventValues(self,data):
        pTitle = data["post_title"]
        pBody = data["post_body"]
        aID = data["author_id"]
        participants = "{" + data["participants"] + "}"
        return tuple([pTitle,pBody,aID,participants])
    
    userTemplate = {
        "username":"TEXT",
        "student_name":"TEXT", 
        "affiliation":"TEXT",
        "ss_ranking":"INT",
        "personality_traits":"[TEXT,...]"
    }

    eventTemplate = {
        "post_title": "TEXT",
        "post_body": "TEXT",
        "author_id": "INT",
        "participants": "INT[]"
    }

    Query_table = {
    1: ("user_insert", 5 ,"""
        INSERT INTO users (username, student_name, affiliation, ss_ranking, personality_traits)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    ""","python3 DatabaseUI.py -s 1 -v blackBolt \"Levinthus Phoenix\" \"Phoenix\" \"3 Stars\" \"Soul Searching\""),
    2: ("event_insert", 2 ,"""
        INSERT INTO events (post_title, post_body, author_id, participants)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    ""","python3 DatabaseUI.py -s 2 -v \"Ghosts on Campus\" \"Has anyone noticed the strange activity in the plaza\""),
    3: ("user_get_all",0, "SELECT * FROM users;","python3 DatabaseUI.py -s 3"),
    4: ("event_get_all",0, "SELECT * FROM events;","python3 DatabaseUI.py -s 4"),
    5: ("user_get_specfic",1, """
        SELECT * FROM users
        WHERE {col} = %s;""","python3 DatabaseUI.py -s 5 -f student_name -v \"Levinthus Phoenix\""),
    6: ("event_get_specfic",1, """
        SELECT * FROM events
        WHERE {col} = %s;""","python3 DatabaseUI.py -s 6 -f post_title -v \"Ghosts on Campus\""),
    7: ("user_update",2,"""
        UPDATE users
        SET {col} = %s WHERE {col2} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 7 -f username student_name -v PhoenixPrince \"Levinthus Phoenix\""),
    8: ("event_update",2,"""
        UPDATE events
        SET {col} = %s WHERE {col2} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 8 -f post_body post_title -v \"HEEEELLLLPP GHOSTS ARE ATTACKING ME\" \"Ghosts on Campus\""),
    9: ("user_delete",1,"""
        DELETE FROM users
        WHERE {col} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 9 -f student_name -v \"Levinthus Phoenix\""),
    10: ("event_delete",1,"""
        DELETE FROM events
        WHERE {col} = %s
        RETURNING *;""","python3 DatabaseUI.py -s 10 -f post_title -v \"Ghosts on Campus\"")
    }
