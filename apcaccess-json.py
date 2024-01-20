#!/usr/bin/env python3
# https://github.com/flyte/apcaccess/blob/develop/apcaccess/status.py
import socket


CMD_STATUS = b"\x00\x06status"
EOF = b"  \n\x00\x00"
SEP = ":"
BUFFER_SIZE = 1024


def get(host: str="localhost", port: int=3551, timeout: int=30) -> str:
    """
    Connect to the APCUPSd NIS and request its status.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))
    sock.send(CMD_STATUS)
    buffr = b""
    while not buffr.endswith(EOF):
        buffr += sock.recv(BUFFER_SIZE)
    sock.close()
    return buffr.decode()


def split(raw_status: str) -> list:
    """
    Split the output from get_status() into lines, removing the length and
    newline chars.
    """
    # Remove the EOF string, split status on the line endings (\x00), strip the
    # length byte and newline chars off the beginning and end respectively.
    return [x[1:-1] for x in raw_status[:-len(EOF)].split("\x00") if x]


def parse(raw_status: str) -> dict:
    """
    Split the output from get_status() into lines, clean it up and return it as
    an OrderedDict.
    """
    lines = split(raw_status)
    # Split each line on the SEP character, strip extraneous whitespace and
    # create an OrderedDict out of the keys/values.
    return dict([[x.strip() for x in x.split(SEP, 1)] for x in lines])


if __name__ == '__main__':
    import json

    HOST = 'localhost'
    PORT = 3551

    print(json.dumps(parse(get(host=HOST, port=PORT))))
