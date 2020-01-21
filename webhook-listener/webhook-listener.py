#!/usr/bin/python2

import hmac
import json
import logging
import ast
from flask import Flask, request
from flask_restplus import Api, Resource, fields
app = Flask(__name__)
api = Api(app, version="1.1", title="NetBox Webhook Listener",
        description="Tested with NetBox 2.6.6")
ns = api.namespace("webhook")
APP_NAME = "webhook-listener"
WEBHOOK_SECRET = "My precious"
#LOG_PATH = "/webhook/" + APP_NAME
LOG_PATH = APP_NAME
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_logging = logging.FileHandler("{}.log".format(LOG_PATH))
file_logging.setFormatter(formatter)
logger.addHandler(file_logging)
webhook_request = api.model("Webhook request from NetBox", {
    'username': fields.String,
    'data': fields.Raw(description="The object data from NetBox"),
    'event': fields.String,
    'timestamp': fields.String,
    'model': fields.String,
    'request_id': fields.String,
})
def do_something_with_the_event(data):
    logger.info(data)
    pass
@ns.route("/")
class WebhookListener(Resource):
    @ns.expect(webhook_request)
    @ns.doc(responses={200: "Ok", 400: "Bad request"})
    def post(self):
        if request.content_length > 1000000:
            # To prevent memory allocation attacks
            logger.error("Content too long ({})".format(
                request.content_length
            ))
            return {"result": "Content too long"}, 400
        input_data = request.get_data()
        #x_hook_signature = request.headers.get("X-Hook-Signature")
        #if x_hook_signature:
        #    input_hmac = hmac.new(
        #        key=WEBHOOK_SECRET.encode(),
        #        msg=input_data,
        #        digestmod="sha512"
        #    )
        #    if not hmac.compare_digest(
        #            input_hmac.hexdigest(),
        #            x_hook_signature):
        #        logger.error("Invalid message signature")
        #        return {"result": "Invalid message signature"}, 400
        #    logger.info("Message signature checked ok")
        #else:
        #    logger.info("No message signature to check")
        try:
            input_dict = json.loads(input_data)
        except json.JSONDecodeError:
            input_dict = None
        if not input_dict or "model" not in input_dict:
            logger.error("Invalid input: {}".format(input_data))
            return {"result":"Invalid input"}, 400

### Unicode in dicts
#        dicts = {}
#        for i, v in input_dict.items():
#          ky = i.encode('ascii','ignore')
#          # If value is dict too, then make it non-unicode
#          if type(v) is dict:
#            dictn = {} 
#            for k, m in v.items():
#                kv = k.encode('ascii', 'encode')
#                if type(m) is dict:
#                  for a,b in m.items():
#                      dictm = {}
#                      ae = a.encode('ascii', 'encode')
#                      if b is str:
#                        dictm[ae] = b.encode('ascii', 'encode')
#                elif m is None:
#                     dictm[ae] = None
#                elif type(m) is int:
#                     dictm[ae] = m
#                elif type(m) is list:
#                  dictm[ae] = [ item.encode('ascii') for item in m ]
#                else:
#                    dictm[ae] = m.encode('ascii', 'encode')
#                dictn[kv] = dictm
#            v = dictn
#            dicts[ky] = v
#          if type(v) is list:
#              dicts[ky] = [ item.encode('ascii') for item in v ]
#          elif type(v) is dict:
#                  for a,b in v.items():
#                      dictm = {}
#                      ae = a.encode('ascii', 'encode')
#                      if b is str:
#                        dictm[ae] = b.encode('ascii', 'encode')
#                      dicts[ky] = dictm
#          else: dicts[ky] = v.encode('ascii','ignore')
#        input_dict=dicts
###        
        do_something_with_the_event(input_dict)
        return {"result":"ok"}, 200
if __name__ == "__main__":
    app.run(host="0.0.0.0")