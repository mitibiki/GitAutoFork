# -*- coding:utf-8 -*-  
from settings import *
global NAME
global PASSWORD
global GITNAME
global GITPASSWORD
import sys
import requests
import json
import traceback
import time
from requests.auth import HTTPBasicAuth
reload(sys)
sys.setdefaultencoding('utf-8')
#url = "https://api.github.com/repos/peng8350/JPTabBar/forks"
class Gitstar():
	def __init__(self,url=""):
		self.NAME 		= NAME
		self.PASSWORD 		= PASSWORD
		self.GITNAME 		= GITNAME
		self.GITPASSWORD 	= GITPASSWORD

		self.cookie = None
	def loginGitStar(self):
		r=requests.post("http://gitstar.top:88/api/user/login",params={'username':self.NAME,'password':self.PASSWORD})
		self.cookie = r.headers['Set-Cookie']
		return r.headers['Set-Cookie']
	def getGitForkList(self):

		cookie=self.loginGitStar()
		url="http://gitstar.top:88/api/users/{}/status/fork-recommend".format(self.NAME)
		response = requests.get(url,headers={'Accept': 'application/json','Cookie':cookie})
		jsn=response.json()

		list=[]
		for obj in jsn:
			list.append(obj['Repo'])
		return list
	def fork(self,url):
		global AUTH

		AUTH = HTTPBasicAuth(self.GITNAME, self.GITPASSWORD)
		print url;
		res = requests.post("https://api.github.com/repos/"+url+"/forks"
			,headers={'Content-Length': '0'}
			,auth=AUTH);
	def update_gitstar(self):
		url = "http://gitstar.top:88/api/users/{}/forking-repos/update".format(self.NAME)
		res = requests.get(url,headers={'Accept': 'application/json','Cookie':self.cookie})
		print "update:" + str(res.status_code == 200)

GS=Gitstar()
urls = GS.getGitForkList()
print "get total github repo:%d" % len(urls)
i = 1
for url in urls:
	GS.fork(url)
	print "[%d]Forked! -->%s"%(i,url)
	time.sleep(5.0)
	i = i + 1
if len(urls) > 0:
	GS.update_gitstar()