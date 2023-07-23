from os import environ
import traceback
import logging
import requests
import sqlite3
import json
import sys
from lib.genesis import genesis
from lib.helpers import *
import pickle, base64
import os

os.remove("database.db") 

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# connects to internal database
con = sqlite3.connect("database.db")
con.row_factory = sqlite3.Row

# call genesis function to setup rules table and setup initial rules
genesis(con)


# Helps in posting to one of the endpoints like notice, report or voucher
def post(endpoint, payloadStr, logLevel):
    logger.log(logLevel, f"Adding {endpoint} with payload: {payloadStr}")
    payload = str2hex(payloadStr)
    response = requests.post(f"{rollup_server}/{endpoint}", json={"payload": payload})
    logger.info(f"Received {endpoint} status {response.status_code} body {response.content}")

def call_rule(rule_name, metadata, cur, data):
    cur.execute(f'SELECT * FROM RULES WHERE name="{rule_name}"')
    result = [{k:r[k] for k in r.keys()} for r in cur.fetchall()]
    try:
        exec(hex2str(result[0]["logic"]))
        return locals()[rule_name](metadata, cur, data)
    except Exception as e:
        return {"error": e}


def handle_request(data, request_type):
    cur = con.cursor()
    try:
        payload = json.loads(hex2str(data["payload"]))  
        ERC20PortalAddress = "0x4340ac4FcdFC5eF8d34930C96BBac2Af1301DF40"

        if request_type == "advance_state":
            if data["metadata"]["msg_sender"].lower() == ERC20PortalAddress.lower():
                result = handle_erc20_deposit(data, cur)
                post("notice", json.dumps(result, default=str), logging.INFO)
            else:        
                result = call_rule(payload["action"], payload["metadata"], cur, data)
                post("notice", json.dumps(result, default=str), logging.INFO)
        else:
            result = call_rule(payload["action"], payload["metadata"], cur, data)
            post("report", json.dumps(result, default=str), logging.INFO)
        return "accept"
    except:
        return "reject"
finish = {"status": "accept"}



while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        finish["status"] = handle_request(rollup_request["data"], rollup_request["request_type"])
