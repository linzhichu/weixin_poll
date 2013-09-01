# -*- coding:utf-8 -*-
import re
from random import randint
from django.shortcuts import render_to_response
import urllib,urllib2,time,hashlib  
from django.http import HttpResponse

from polls.models import WexinInfo
from polls.models import *

TOKEN = "weixinpoll"

def home(request):
	return render_to_response('index.tpl',{})

import xml.etree.ElementTree as ET  
import urllib,urllib2,time,hashlib  

from django.http import HttpResponse, HttpResponseRedirect  
from django.template import RequestContext, Template  
from django.views.decorators.csrf import csrf_exempt  
from django.utils.encoding import smart_str, smart_unicode  
from django.shortcuts import render_to_response


class MsgType(object):
    
    def __init__(self, funcflag=False):
        self.funcflag = funcflag
    
    def get_ret_xml(self, msg):
        container = '''
<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
%s
    <FuncFlag>%s</FuncFlag>
</xml>'''
        
        content = self.get_xml()
        full_xml = container %(msg['FromUserName'], msg['ToUserName'], str(int(time.time())), content, '1' if self.funcflag else '0')
        return full_xml
    
    def get_xml(self):
        return ''


class Text(MsgType):

    xmltempl = '''
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
'''
    
    def __init__(self,text, funcflag=False):
        super(Text, self).__init__(funcflag)
        self.text = text

    def get_xml(self):
        if self.text:
            xmltempl = self.xmltempl % ('text', self.text)
        else:
            xmltempl = None
        return xmltempl


class Music(MsgType):

    xmltempl = '''
 <MsgType><![CDATA[music]]></MsgType>
 <Music>
 <Title><![CDATA[%s]]></Title>
 <Description><![CDATA[%s]]></Description>
 <MusicUrl><![CDATA[%s]]></MusicUrl>
 <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
 </Music>
'''
    def __init__(self, title, desc, musicurl, hqurl, funcflag=False):
        self.title = title
        self.desc = desc
        self.musicurl = musicurl
        self.hqurl = hqurl

    def get_xml(self):
        try:
            return xmltempl %(self.title, self.desc, self.musicurl, self.hqurl)
        except:
            return None

class News(MsgType):
    xmltempl = '''
 <MsgType><![CDATA[news]]></MsgType>
 <ArticleCount>2</ArticleCount>
 <Articles>
 <item>
 <Title><![CDATA[title1]]></Title> 
 <Description><![CDATA[description1]]></Description>
 <PicUrl><![CDATA[picurl]]></PicUrl>
 <Url><![CDATA[url]]></Url>
 </item>
 <item>
 <Title><![CDATA[title]]></Title>
 <Description><![CDATA[description]]></Description>
 <PicUrl><![CDATA[picurl]]></PicUrl>
 <Url><![CDATA[url]]></Url>
 </item>
 </Articles>
'''
    articlelimit = 10
    pass

class Image(MsgType):
    xmltempl = '''
 <MsgType><![CDATA[image]]></MsgType>
 <PicUrl><![CDATA[%s]]></PicUrl>
'''
    def __init__(self, picurl, funcflag=False):
        super(Image, self).__init__(self, funcflag)
        self.picurl = picurl

    def get_xml(self):
        if picurl:
            return xmltempl %(self.picurl)
        else:
            return None

class Link(MsgType):
    xmltempl = '''
<MsgType><![CDATA[link]]></MsgType>
<Title><![CDATA[公众平台官网链接]]></Title>
<Description><![CDATA[公众平台官网链接]]></Description>
<Url><![CDATA[url]]></Url>
'''
    def __init__(self, title, desc, url):
        self.title = title
        self.description = desc
        self.url = url


class Location(MsgType):
    
    xmltempl = '''
<MsgType><![CDATA[location]]></MsgType>
<Location_X>23.134521</Location_X>
<Location_Y>113.358803</Location_Y>
<Scale>20</Scale>
<Label><![CDATA[位置信息]]></Label>
'''
    def __init__(self, loc_x, loc_y, scale, label):
        self.location_x = loc_x
        self.location_y = loc_y
        self.scale = scale
        self.label - label
    pass

class WeixinBase(object):

    def __init__(self, request):
        rawStr = smart_unicode(request.raw_post_data)
        #import code;code.interact(local=locals())
        print rawStr
        msg = parseMsgXml(ET.fromstring(rawStr))  
        self.msg_dict = msg
        
        self.fromuser = self.getfromuser()
    def response_msg(self):
        msg_handler = {
            "text": (self.response_text, self.get_text) ,
            "event": (self.process_event, None) ,
            }
        msgtype = self.msg_dict['MsgType']
        handler = msg_handler.get(msgtype, None)
        if handler[1]:
            ret_obj = handler[0](handler[1]())
        else:
            ret_obj = handler[0]()
            
        return ret_obj.get_ret_xml(self.msg_dict)
        
    def process_event(self):
        event_handler = {
            "subscribe": self.response_subscribe,
            "unsubscribe": self.response_unsubscribe,
            }
        handler = self.msg_dict.get('Event', None)
        if handler:
            return event_handler[handler]()
        else:
            return None

    def response_subscribe(self):
	    return Text('welcome')
            pass
            
    def response_unsubscribe(self):
        pass

    def response_text(self, text):
        #msg = text.text
        msg = self.proc_response(text.text)
        replymsg = u"I can say:"+ msg
			
        return Text(replymsg)

    def response_music(self, music):
        return None

    def getfromuser(self):
        return self.msg_dict['FromUserName'].strip()

    def get_text(self):
        return Text(self.msg_dict.get('Content', None))
    
    def get_music(self):
        return None

    def proc_response(self, text):
	    if text.startswith("#"):
		    text = self.responder_msg(text)
	    elif text.startswith("TouPiao:"):
		    text =self.creater_msg(text)
	    #text = self.getfromuser()
	    return text

    def creater_msg(self, text):
	    activity_desc = text.lstrip(u"创建 ")
	    activity_slug = randint(100,999)
	    activity = Activity.objects.create(description=activity_desc,slug=activity_slug)
	    activity.save()
	    poll_pattern = re.compile(r'\d+\:\S+')
	    polls = re.findall(poll_pattern, text)
	    if len(polls)>0:
		    for index, poll in enumerate(polls):
			    poll=Poll.objects.create(activity=activity, poll_id=index+1, poll_text=poll.split(":")[1], votes=0)
			    poll.save()
	    return "欢迎使用投票助手，请回复 #%s 选项 进行投票"%activity.slug + "%s"%text.lstrip("创建 ")

    def responder_msg(self, text):
	    return text

def handleRequest(request, wxclass=WeixinBase):  
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response  
    elif request.method == 'POST':
        wx = wxclass(request)
        re_msg = wx.response_msg()
        response = HttpResponse(re_msg,content_type="application/xml")
        return response  
    else: 
        return None 
 
def checkSignature(request):  
    global TOKEN  
    signature = request.GET.get("signature", None)  
    timestamp = request.GET.get("timestamp", None)  
    nonce = request.GET.get("nonce", None)  
    echoStr = request.GET.get("echostr",None)  
  
    token = TOKEN  
    tmpList = [token,timestamp,nonce]  
    tmpList.sort()  
    tmpstr = "%s%s%s" % tuple(tmpList)  
    tmpstr = hashlib.sha1(tmpstr).hexdigest()  
    if tmpstr == signature:  
        return echoStr
    else:  
        return None  
  
def parseMsgXml(rootElem):  
    msg = {}
    if rootElem.tag == 'xml':  
        for child in rootElem:  
            msg[child.tag] = smart_unicode(child.text).strip()  
            print child.tag, msg[child.tag]
    #import code; code.interact(local=locals())
    return msg

