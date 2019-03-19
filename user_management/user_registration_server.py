#!/usr/bin/env python3
"""
Listens for user data from the website and adds them to the mongodb
server to be used for sending emails
"""

import io
import json

from http.server import HTTPServer, BaseHTTPRequestHandler

import pymongo

USERINFO_DB = None

class HTTPRegistrationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body_len = int(self.headers['Content-Length'])
        body = self.rfile.read(body_len)
        print(f'Recieved data: {body}')
        if register_user(body):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'User registered')
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Unkown Error')

def register_user(data):
    """registers a user from json data"""
    if USERINFO_DB is None:
        # failed to get db connection
        return False

    users = USERINFO_DB['users']
    data = json.loads(data)
    # TODO: validate json
    # TODO: validate user (duplicates?)
    users.insert_one(data)

    return True
    

def main():
    """connects to db and listens"""
    db_client = pymongo.MongoClient("mongodb://localhost:27017/")
    global USERINFO_DB
    USERINFO_DB = db_client['userinfo']
    server = HTTPServer(('localhost', 8000), HTTPRegistrationHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
