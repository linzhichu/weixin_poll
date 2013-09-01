from django.db import models

# Create your models here.

class Activity(models.Model):
    description = models.CharField(max_length=200)
    slug = models.CharField(max_length=6)
    def __unicode__(self):
        return "%s %s"%(self.slug, self.description)


class Poll(models.Model):
    activity = models.ForeignKey(Activity)
    poll_id = models.IntegerField()
    poll_text = models.CharField(max_length=20)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return "%s:%s"%(self.poll_id, self.poll_text)

class WexinInfo(models.Model):
    secret = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)
    nonce = models.CharField(max_length=100)
    echostr = models.CharField(max_length=100)

class WeixinUser(models.Model):
    weixin_id = models.CharField(max_length=100)
    subscript = models.BooleanField(default=False)
