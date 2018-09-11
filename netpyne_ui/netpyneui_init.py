"""
netpyne_geppetto_init.py
Initialise NetPyNE Geppetto, this class contains methods to connect NetPyNE with the Geppetto based UI
"""
import traceback
import json
import logging
from jupyter_geppetto.geppetto_comm import GeppettoJupyterModelSync, GeppettoJupyterGUISync

def getJSONError(message, details):
    data = {}
    data['type'] = 'ERROR'
    data['message'] = message
    data['details'] = details
    return json.dumps(data)

def getJSONReply():
    data = {}
    data['type'] = 'OK'
    return json.dumps(data)

logging.info("NetPyNEUIInit init method was called")
from netpyne_ui import netpyne_geppetto
netpyne_geppetto = netpyne_geppetto.NetPyNEGeppetto()
GeppettoJupyterModelSync.events_controller.triggerEvent("spinner:hide")
logging.info("NetPyNEUIInit object was instantiated")