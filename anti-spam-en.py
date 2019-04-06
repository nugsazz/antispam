# -*- coding: utf-8 -*-
from Line.linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse,timeit,atexit
from time import strftime
#==================================================================================================================#
me = LINE()
me.log("Auth Token : " + str(me.authToken))
meMID = me.profile.mid
botStart = time.time()
oepoll = OEPoll(me)
Me = [meMID,"u6949f816dddef051b5762322e5597f1e","ufe1707ae9b2ff7ab61505795b7995440"]
#==================================================================================================================#
def restartBot():
    print ("[ Info ] Bot Restart")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def logError(text):
    me.log("[ Error ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@yinmo©2019 "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mid")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    me.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
#==================================================================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            sendMention(op.param1, " @! Thanks For Add Me",[op.param1])
            sendMention(op.param1, " @! Sorry AutoBlock On",[op.param1])
            me.blockContact(op.param1)
        if op.type == 6:
            contact = me.getContact(op.param1)
            print ("[ 6 ] {} has been blocked".format(contact.displayName) + " Mid: " + contact.mid )
        if op.type == 13:
            if meMID in op.param3:
               group = me.getGroup(op.param1)
               inviter= me.getContact(op.param2)
               print ("[ 13 ] " + inviter.displayName + " invite you" + str(group.name))
               if str(group.name).lower() in ["邀機","test","spam","邀機降臨","測試","。","幹","幹你娘","fuck"]:
                  me.rejectGroupInvitation(op.param1)
               elif len(group.members) < 5:
                  me.rejectGroupInvitation(op.param1)
        if op.type == 21 or op.type == 22 or op.type ==24:
            print ("[ NOTIFY LEAVE ROOM ]")
            me.leaveRoom(op.param1)
        if (op.type == 25 or op.type == 26) and op.message.contentType == 0:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != me.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if 'ORGCONTP' in msg.contentMetadata.keys()!= None and msg.contentMetadata['ORGCONTP'] == "CALL":
                if msg.contentMetadata['GC_EVT_TYPE'] == "I":
                    me.sendMessage(sender, "DON'T INVITE ME GROUP CALL")
                    me.blockContact(sender)
            if sender in Me:
                if text.lower() in ['speed','sp']:
                    me.sendReplyMessage(msg.id, to,"About"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000)) + "secs")
                elif text.lower() == 'runtime':
                       me.sendReplyMessage(msg.id, to, "System run {}".format(str(format_timespan(time.time() - botStart))))
                elif text.lower() == 'restart':
                       me.sendReplyMessage(msg.id, to, "Restart Done")
                       restartBot()
    except Exception as error:
        logError(error)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except:
        pass
        
        
