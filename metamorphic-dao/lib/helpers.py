from .eth_abi_ext import decode_packed
from eth_abi import encode
import requests, json
from os import environ
import logging, requests

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")


def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()


def post(endpoint, payloadStr, logLevel):
    logger.log(logLevel, f"Adding {endpoint} with payload: {payloadStr}")
    payload = str2hex(payloadStr)
    response = requests.post(f"{rollup_server}/{endpoint}", json={"payload": payload})
    logger.info(f"Received {endpoint} status {response.status_code} body {response.content}")

def fetch_all(query, cursor):
    cursor.execute(query) 
    return [{k:r[k] for k in r.keys()} for r in cursor.fetchall()]

def handle_erc20_deposit(data, cur):
    binary = bytes.fromhex(data["payload"][2:])
    try:
        success, erc20, depositor, amount = decode_packed(['bool','address','address','uint256'], binary)
        requests.post(rollup_server + "/report", json=json.dumps({"type":"deposit", 'from':depositor,'amount':amount}))
        if success:
            cur.execute("CREATE TABLE IF NOT EXISTS OWNERSHIPS (erc20_address text, depositor_address text, amount text)")
            cur.execute("INSERT INTO OWNERSHIPS (erc20_address,depositor_address,amount) VALUES(?,?,?)",[erc20, depositor, amount])
            return {"type":"deposit", 'from':depositor,'amount':amount}
    except Exception as e:
        return {'error':"rejected"}

def handle_erc20_withdraw(recipient, amount, erc20_contract_address):
    TRANSFER_FUNCTION_SELECTOR = b'\xa9\x05\x9c\xbb'
    transfer_payload = TRANSFER_FUNCTION_SELECTOR + encode(['address','uint256'], [recipient, amount])
    voucher = {"destination": erc20_contract_address, "payload": "0x" + transfer_payload.hex()}
    requests.post(rollup_server + "/voucher", json=voucher)