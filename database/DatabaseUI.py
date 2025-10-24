import argparse
import psycopg2
from psycopg2.extras import execute_batch, execute_values, RealDictCursor
import os
from dotenv import load_dotenv
from utils.bot_logger import setup_logger
load_dotenv(dotenv_path="db.env")
Query_table = {
    1: ("user_insert", 5 ,"""
        INSERT INTO users (username, student_name, affiliation, ss_ranking, personality_traits)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """),
    2: ("event_insert", 2 ,"""
        INSERT INTO events (event_name, post_id)
        VALUES (%s, %s)
        RETURNING id;
    """)
}

class UserInterface():

    def __init__(self,_qTable):
        
        self.logger = setup_logger()
        self.logger.debug(f"Logger setup successfully!")
        self.qTable = _qTable

        self.conn = None
        self.get_conn()

    def get_conn(self):
        try:
            self.logger.debug(f"HOST:{os.getenv('POSTGRES_HOST')}")
            self.logger.debug(f"PORT:{os.getenv('POSTGRES_PORT')}")
            self.logger.debug(f"DB:{os.getenv('POSTGRES_DB')}")
            self.logger.debug(f"USER:{os.getenv('POSTGRES_USER')}")
            self.logger.debug(f"PASS:{os.getenv('POSTGRES_PASSWORD')}")
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

    def insertQuery(self,_query,_val,_type):
        try:
            with self.conn as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(_query, _val)
                    new_user = cur.fetchone()
                    conn.commit()
                    # self.logger.info(f"✅ Inserted user '{new_user['student_name']}' with id {new_user['id']}")
        except psycopg2.errors.UniqueViolation:
            self.logger.error(f"⚠️ {_type} already exists — skipping insert.")
        except psycopg2.Error as e:
            self.logger.error(f"❌ Database error inserting {_type} : {e}")
            exit()



    def startQuery(self,_qID,_query,_val):
        
        if _qID == 1:
            _array = "{" + _val[4] + "}"
            _val[4] = _array
            self.insertQuery(_query,tuple(_val),'user')
        elif _qID == 2:
            self.insertQuery(_query,tuple(_val),'event')

def main(argv):

    _db = UserInterface(Query_table)

    if argv.json_import:
        pass

    if argv.select_template and argv.values:
        _recieved = len(argv.values)
        _expected = Query_table[int(argv.select_template)][1]
        if  _recieved != _expected:
            _db.logger.error(f"Passed in {_recieved} values but expected {_expected}... ")
            exit()
        
        _qStr = Query_table[int(argv.select_template)][2]
        _db.startQuery(int(argv.select_template),_qStr,argv.values)
        _db.logger.info(f"Query ran successfully!")





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="User Interface to make trivialize database interaction",formatter_class=argparse.RawTextHelpFormatter)

    # parser.add_argument('-t','--table',required=True, type=str, nargs=1, help="table to maniputate [users/events]")
    parser.add_argument('-j','--json_import',type=str,nargs=1,help="Requires a json file to read from")
    parser.add_argument('-s','--select_template',choices=['1','2','3'],help="choices " + ", ".join(f"\n{k}: {v[0]}" for k,v in Query_table.items()))
    parser.add_argument('-v','--values',type=str,nargs='*',help="Requires -s to make a selection of a template")
    args = parser.parse_args()
    main(args)