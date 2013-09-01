from django.shortcuts import render_to_response
import urllib,urllib2,time,hashlib  
from django.http import HttpResponse

from polls.models import WexinInfo

def home(request):
	return render_to_response('index.tpl',{})

def getSignature(request):
    rawStr = smart_unicode(request.raw_post_data)
    #import code;code.interact(local=locals())
    msg = parseMsgXml(ET.fromstring(rawStr))  
    self.msg_dict = msg
    pass

def handleRequest(request):  
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response  
    elif request.method == 'POST':
        pass
        #re_msg = wx.response_msg()
        re_msg = response_msg()
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
    
    #WexinInfo.objects.create(secret=signature,timestamp=timestamp,nonce=nonce,echostr=echoStr)

    
    token = TOKEN  
    tmpList = [token,timestamp,nonce]  
    tmpList.sort()  
    tmpstr = "%s%s%s" % tuple(tmpList)  
    tmpstr = hashlib.sha1(tmpstr).hexdigest()  
    if tmpstr == signature:  
        return echoStr
    else:  
        return None