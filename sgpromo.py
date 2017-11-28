# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser
import json

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

ongoing = "http://singpromos.com/bydate/ontoday/"
tdy = 'http://singpromos.com/bydate/startedtoday/'
tmr = 'http://singpromos.com/bydate/startingtmw/'
soon = 'http://singpromos.com/bydate/comingsoon/'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)


class Main(Wox):
  
    def request(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
	#get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
	    proxies = {
		"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
		"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
	    }
	    return requests.get(url,proxies = proxies, headers=headers)
	return requests.get(url, headers=headers)
			
    def query(self, param):
        if param.strip() == 'today':
            r = self.request(tdy)
        elif param.strip() == 'tmr':
            r = self.request(tmr)
        elif param.strip() == 'soon':
            r = self.request(soon)
        else:
            r = self.request(ongoing)
	
	
	bs = BeautifulSoup(r.content, 'html.parser')
        feeds = bs.select('div[class="tabs1Content"] article')

	result = []
	for f in feeds:
            fa = f.find('h3').find('a')
            falink = fa['href']
            fb = f.find('div', class_='mh-excerpt').find('p')
            post = {
                    'Title': fa.text.strip(),
                    'SubTitle': fb.text[:99] + ' ...',
                    'IcoPath': os.path.join('img', 'sgpromo.png'),
                    'JsonRPCAction': {
                        'method': 'open_url',
                        'parameters': [falink]
                    }
                }
            result.append(post)
        if not result:
            result.append({
                    'Title': 'No News Now'
                })
        
	return result
    
    def open_url(self, url):
	webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)

if __name__ == '__main__':
    Main()
