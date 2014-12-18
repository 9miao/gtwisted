#coding:utf8
'''
Created on 2014年2月21日

@author:  lan (www.9miao.com)
'''
from gtwisted.core import reactor
from flask import Flask
import json

app = Flask(__name__)
app.debug = True

@app.route("/test", methods=["GET"])
def poll():
    print 123
    return "hello word!!"

reactor.listenWSGI(1800, app)
reactor.run()






