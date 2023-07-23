from .helpers import *

create_ammendment_proposal = '''
def create_ammendment_proposal(metadata, cur, data):
    cur.execute("INSERT INTO AMMENDMENT_PROPOSALS (name,logic,description) VALUES(?,?,?)",[metadata["name"], metadata["logic"], metadata["description"]]);'''

delete_ammendment_proposal = '''
def delete_ammendment_proposal(metadata, cur, data):
    proposal_name = metadata["name"]
    cur.execute(f'DELETE FROM AMMENDMENT_PROPOSALS WHERE name="{proposal_name}"')
'''

genesis_ammendment_concensus_rule = '''
def ammendment_concensus(metadata, cur, data):
    # Our initial consensus rule is to just take ammendment name from ammendment proposals table and add it to rules table
    proposal = metadata["name"]
    cur.execute(f'SELECT * FROM AMMENDMENT_PROPOSALS WHERE name="{proposal}"')
    ammendment_data = cur.fetchall()
    cur.execute("INSERT INTO RULES (name,logic,description) VALUES(?,?,?)",[ammendment_data[0]["name"], ammendment_data[0]["logic"], ammendment_data[0]["description"]])
    cur.execute(f'DELETE FROM AMMENDMENT_PROPOSALS WHERE name="{proposal}"')
'''

table_info = '''
def table_info(metadata, cur, data):
    table_name = metadata["name"]
    listOfTables = cur.execute(f'SELECT tbl_name FROM sqlite_master WHERE type="table" AND tbl_name="{table_name}"; ').fetchall()
    if listOfTables == []:
        return {'error': f'Table {table_name} not found'}
    else:
        cur.execute(f'SELECT * FROM "{table_name}"')
        return [{k:r[k] for k in r.keys()} for r in cur.fetchall()]
'''

def genesis(con):
    cur = con.cursor()

    # type could be create, update, delete
    cur.execute("CREATE TABLE IF NOT EXISTS AMMENDMENT_PROPOSALS (name text, logic text, description text, expiry timestamp, votes int)")
    cur.execute("CREATE TABLE IF NOT EXISTS RULES (name text, logic text, description text)")

    # Add CRUD Rules for ammendment proposals, and add genesis concesus rules 
    cur.execute("INSERT INTO RULES (name,logic,description) VALUES(?,?,?)",['create_ammendment_proposal', str2hex(create_ammendment_proposal), 'Create ammendment proposal'])
    cur.execute("INSERT INTO RULES (name,logic,description) VALUES(?,?,?)",['delete_ammendment_proposal', str2hex(delete_ammendment_proposal), 'Delete ammendment proposal'])
    cur.execute("INSERT INTO RULES (name,logic,description) VALUES(?,?,?)",["ammendment_concensus", str2hex(genesis_ammendment_concensus_rule), "Rules for ammendment_concensus in the DAO at genesis"])
    cur.execute("INSERT INTO RULES (name,logic,description) VALUES(?,?,?)",["table_info", str2hex(table_info), "Getting information about a table"])




