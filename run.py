#from aiohttp import web
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys
import time
import requests
import telebot

HOSTNAME = os.getenv('HOSTNAME', "0.0.0.0")
PORT = os.getenv('PORT', 9000)

TLGRM_URL = os.getenv('TLGRM_URL')
TLGRM_API_TOKEN = os.getenv('TLGRM_API_TOKEN')
TLGRM_CHAT_ID = os.getenv('TLGRM_CHAT_ID')
SEND_POST_ELEMENT = os.getenv('SEND_POST_ELEMENT')

if TLGRM_URL is None or TLGRM_API_TOKEN is None or TLGRM_CHAT_ID is None or SEND_POST_ELEMENT is None:
    sys.exit('Please set env: TLGRM_URL TLGRM_API_TOKEN TLGRM_CHAT_ID SEND_POST_ELEMENT')

bot = telebot.TeleBot(TLGRM_API_TOKEN)

class WebApp(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(json.loads(post_data.decode('utf-8'))[SEND_POST_ELEMENT])
        bot.send_message(TLGRM_CHAT_ID, json.loads(post_data.decode('utf-8'))[SEND_POST_ELEMENT] )

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Proxy</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>Proxy is running</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


Server = HTTPServer((HOSTNAME, PORT), WebApp)

print(time.asctime(), "Server Starts - %s:%s" % (HOSTNAME, PORT))

try:
    Server.serve_forever()
except KeyboardInterrupt:
    pass

Server.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (HOSTNAME, PORT))
