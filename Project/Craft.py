import websocket
import threading

import os
import json
import uuid
import sys

from time import sleep
from json import JSONEncoder
from uuid import UUID

JSONEncoder_olddefault = JSONEncoder.default

#special encoding for supporting UUID in json payload
def JSONEncoder_newdefault(self, o):
	if isinstance(o, UUID): return str(o)
	return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_newdefault



class CraftClient(object):
	def __init__(self):
		self.executableName=""
		self.manifestPath=""
		self.callback=""

	def on_message(self,ws, message):
		# craft events come in as json objects 
		craftEventObj = json.loads(message)
		if self.callback:
		   self.callback(craftEventObj)
	
	def on_close(self,ws):
		print ("### closed ###")

	def on_open(self,ws):
		uid = uuid.uuid1()
		pid = os.getpid()
	
		connectMessage = {
			"message_type": "register",
			"plugin_guid": uid,
			"PID": pid,
			"execName": self.executableName,
			"manifestPath": self.manifestPath
		}
	
		regMsg =  json.dumps(connectMessage)		
		ws.send(regMsg.encode('utf8'))

	def connect(self, execName,manifestFilePath):
		self.executableName = execName
		self.manifestPath = manifestFilePath
	
		websocket.enableTrace(True)
		ws = websocket.WebSocketApp("ws://127.0.0.1:10134", 
								 on_open = self.on_open, 
								 on_message = self.on_message, 
								 on_close = self.on_close)
	
		wst = threading.Thread(target=ws.run_forever)
		wst.daemon = True
		wst.start()
		
	def registerEventHandler(self,cb):
		self.callback = cb;

# local test	
#if __name__ == "__main__":
#	connect("CodeRunner.app","")
#	while True:
#		print("waiting for msgs");
#		threading._sleep(1);	
			
