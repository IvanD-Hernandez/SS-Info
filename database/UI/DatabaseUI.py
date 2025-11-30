import argparse
import psycopg2
from psycopg2.extras import execute_batch, execute_values, RealDictCursor
import os
from dotenv import load_dotenv
from psycopg2 import sql
from utils.DButils import DButils

load_dotenv(dotenv_path="db.env")

class UserInterface(DButils):

    def __init__(self):
        super().__init__()

        self.logger.debug(f"Logger setup successfully!")
        self.conn = None
        self.get_conn()
        self.logger.info(f"UserInterface init was a success!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info(f"Closing connection to DB...")
        self.conn.close()

    def get_conn(self):
        try:
            self.logger.debug(f"HOST:{os.getenv('POSTGRES_HOST')}")
            self.logger.debug(f"PORT:{os.getenv('POSTGRES_PORT')}")
            self.logger.debug(f"DB:{os.getenv('POSTGRES_DB')}")
            self.logger.debug(f"USER:{os.getenv('POSTGRES_USER')}")
            self.conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
            self.logger.info("Connected to db!")
        except Exception as e:
            self.logger.error(e)
            exit()

    def sendQuary(self,_query,_val,_type):
        # self.logger.debug(f"Query: {_query}")
        # self.logger.debug(f"Value: {_val}")
        try:
            with self.conn as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    if _val:
                        cur.execute(_query, _val)
                    else:
                        cur.execute(_query)
                    
                    self.logger.debug(f"✅ committing changes to db")
                    conn.commit()
                    
                    if cur.description:  
                        result = cur.fetchall()
                    else:
                        result = None
                    self.logger.debug(f"result: {result}")
                    return result
                    
        except psycopg2.errors.UniqueViolation:
            self.logger.error(f"⚠️ {_type} already exists — skipping insert.")
            return -1
        except psycopg2.Error as e:
            self.logger.error(f"❌ Database error inserting {_type} : {e}")
            exit()

    def sendBulkQuary(self,_query,_valList):
        self.logger.debug(f"query: {_query}")
        self.logger.debug(f"list: {_valList}")
        
        try:
            with self.conn as conn:
                with conn.cursor() as cur:

                    execute_values(cur, _query, _valList)
                    
                    self.logger.debug(f"✅ committing changes to db")
                    conn.commit()
                    
        except psycopg2.errors.UniqueViolation as e:
            self.logger.error(f"⚠️ entry already exists — skipping insert: {e}")
            conn.rollback()
        except psycopg2.Error as e:
            self.logger.error(f"❌ Database error inserting entry : {e}")
            conn.rollback()

    def craftBulkQuery(self,_msgID,_jsonList):
        _res = []
        self.logger.info(f"executing bulk crafting for message type: {_msgID}")
        if _msgID == "1":
            
            for item in _jsonList:
                _res.append(self.getInsertValues(item))
            # self.logger.debug(_res)
            _query = self.templates[int(_msgID)][2].replace("(%s, %s, %s, %s, %s)","%s")

            return(tuple([_query,_res]))
        if _msgID == "2":
            for item in _jsonList:
                _res.append(self.getInsertEventValues(item))
            # self.logger.debug(_res)
            _query = self.templates[int(_msgID)][2].replace("(%s, %s, %s, %s)","%s")

            return(tuple([_query,_res]))    

        else:
            self.logger.warning("Unimplemented type was passed...")
            exit()


    def startQuery(self,argv,_query):
        if isinstance(argv.select_template,str):
            _qID = int(argv.select_template)
        else:
            _qID = argv.select_template
        _val = argv.values
        
        if _qID == 1:
            _array = "{" + _val[4] + "}"
            _val[4] = _array
            _res = self.sendQuary(_query,tuple(_val),self.getQueryIdent(_qID))
            return _res
        
        elif _qID == 2:
            _res = self.sendQuary(_query,tuple(_val),self.getQueryIdent(_qID))
            return _res
        
        elif _qID == 3 or _qID == 4: # Fetch all from table
            _res = self.sendQuary(_query,None,self.getQueryIdent(_qID))
            # self.logger.debug(f"Fetched: {_res}")
            return _res

        elif _qID == 5 or _qID == 6: # Fetch Specific
            if not argv.field:
                self.logger.error(f"This template option requires a single field to be specified, --field")
                return False
            if isinstance(argv.field,list):
                argv.field = argv.field[0]

            _query = sql.SQL(_query).format(col=sql.Identifier(argv.field))
            _res = self.sendQuary(_query,tuple(argv.values),self.getQueryIdent(_qID))
            # self.logger.debug(f"Fetched: {_res}")
            return _res

        elif _qID == 7 or _qID == 8: # Update field at specific
            if not argv.field:
                self.logger.error(f"This template option requires two fields to be specified, --field")
                return False
            
            _field1 = argv.field[0]
            _field2 = argv.field[1]

            _query = sql.SQL(_query).format(col=sql.Identifier(_field1),col2=sql.Identifier(_field2))
            _res = self.sendQuary(_query,tuple(argv.values),self.getQueryIdent(_qID))
            # self.logger.debug(f"Updated: {_res}")
        elif _qID == 9 or _qID == 10: # Delete row
            if not argv.field:
                self.logger.error(f"This template option requires a single field to be specified, --field")
                return False
            if isinstance(argv.field,list):
                argv.field = argv.field[0]

            _query = sql.SQL(_query).format(col=sql.Identifier(argv.field))
            _res = self.sendQuary(_query,tuple(argv.values),self.getQueryIdent(_qID))
            # self.logger.debug(f"Fetched: {_res}")
            return _res

def displayTemplates(_db,_param):
    if _param == '0':
        for key,val in _db.templates.items():
            _db.logger.info(f"{key}: {val[0]} template, {val[1]} values needed {val[2]} \nexample: {val[3]}")
    else:
        key = int(_param)
        val = _db.templates[key]
        _db.logger.info(f"{key}: {val[0]} template, {val[1]} values needed {val[2]} example: {val[3]}")

def main(argv):
    if argv.display_template:
        displayTemplates(DButils(),argv.display_template)
        return

    _db = UserInterface()

    if argv.json_template:
        if argv.json_template =='user':
            _db.genUserTemplate()
        elif argv.json_template =='event':
            _db.genEventTemplate()
        return
    
    if argv.import_json:
        _res = _db.readJson(argv.import_json[0])
        _bulk = []
        for _msgID in _res.keys():
            _bulk.append(_db.craftBulkQuery(_msgID,_res[_msgID]))
        
        for _bulkRequest in _bulk:
            _db.sendBulkQuary(_bulkRequest[0],_bulkRequest[1])

    if argv.select_template:
        
        _expected = _db.getExpected(int(argv.select_template))
        if _expected and argv.values:
            _recieved = len(argv.values)
            if  _recieved != _expected:
                _db.logger.error(f"Passed in {_recieved} values but expected {_expected}... ")
                return
        elif _expected and not argv.values:
            _db.logger.error(f"Expected {_expected} values but recieved none... ")
            return
        
        _qStr = _db.getQueryStr(int(argv.select_template))
        _res =_db.startQuery(argv,_qStr)
        _db.logger.info(f"Query ran successfully!")
        return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="User Interface to make trivialize database interaction",formatter_class=argparse.RawTextHelpFormatter)

    # parser.add_argument('-t','--table',required=True, type=str, nargs=1, help="table to maniputate [users/events]")
    parser.add_argument('-f','--field', type=str, nargs='*',help="Some templates require an id")
    parser.add_argument('-p','--path',type=str,nargs=1,help="works with -i and -e")
    parser.add_argument('-i','--import_json',type=str,nargs=1,help="path of json schema folder")
    # parser.add_argument('-e','--export_json',type=str,nargs=1,help="name of output file")
    parser.add_argument('-j','--json_template',choices=['user','event'],
                        help="Generate a template to fill out")
    parser.add_argument('-s','--select_template',choices=['1','2','3','4','5','6','7','8','9','10'],
                        help="Choose a sql template to use ")
    parser.add_argument('-d','--display_template',nargs='?',const='0',choices=['0','1','2','3','4','5','6','7','8','9','10'],
                        help="Display in depth help on the sql templates ")
    parser.add_argument('-v','--values',type=str,nargs='*',help="Requires -s to make a selection of a template")
    args = parser.parse_args()
    main(args)