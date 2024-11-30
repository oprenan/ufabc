import psycopg2
import logging
import sys
from psycopg2.extras import RealDictCursor

def init_db(conf_hash):

    if conf_hash["pghost"] == None or conf_hash["pgdb"] == None or conf_hash["pguser"] == None or conf_hash["pgpass"] == None:
        logging.fatal("Missing mandatory DB config values - exiting");
        sys.exit("Missing mandatory DB config values - exiting");

    logging.info("Connecting to PG host: {}".format(conf_hash["pghost"]));

    db = {};
    db["connection"] = psycopg2.connect(host=conf_hash["pghost"], dbname=conf_hash["pgdb"], user=conf_hash["pguser"],password=conf_hash["pgpass"]);
    db["cursor"] = db["connection"].cursor(cursor_factory=RealDictCursor)

    return db;

def execute_qry_and_fetch_all_records(db_hash, qry_title, query):

    logging.debug("In execute_qry_and_fetch_records for qry: " + qry_title)
    records = None
    try:
        # Run query to get the admin auth data
        db_hash["cursor"].execute(query)
        if db_hash["cursor"].description != None:
            columns = list(db_hash["cursor"].description)

            row_count = db_hash["cursor"].rowcount
            logging.debug("row_count for {}:  {}".format(qry_title, str(row_count)))

            records = [dict(row) for row in db_hash["cursor"].fetchall()]
        else: 
            logging.info("Numero de linhas: ", db_hash['cursor'].rowcount)

    except Exception as err:
        logging.error("Got error for DB qry [{}]\n\tError: {}\n".format(qry_title,str(err)))
    
    return(records)