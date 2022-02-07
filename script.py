import time
import hashlib
import requests #dependency
import sys
import argparse
from discord import Webhook, RequestsWebhookAdapter
from urllib.request import build_opener, HTTPCookieProcessor

parser = argparse.ArgumentParser()

parser.add_argument('--urlMonitor', type=str, required=True)
parser.add_argument('--discordWebHook', type=str, required=True)

args = parser.parse_args()

urldiscord = args.discordWebHook

url = args.urlMonitor

opener = build_opener(HTTPCookieProcessor())
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
response = opener.open(url).read()
currentHash = hashlib.sha224(response).hexdigest()
print("running")
time.sleep(10)
webhook = Webhook.from_url(urldiscord, adapter=RequestsWebhookAdapter())
webhook.send("@everyone Running for " + url)

while True:
    try:
        response = opener.open(url).read()
    
        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()

        time.sleep(10) 
        
        # perform the get request
        response = opener.open(url).read()
        
        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()

        # check if new hash is same as the previous hash
        if newHash == currentHash:
            
            print("equal")
            continue

        # if something changed in the hashes
        else:
            # notify
            print("something changed")
           
            webhook = Webhook.from_url(urldiscord, adapter=RequestsWebhookAdapter())
            webhook.send("@everyone Something Changed! Visit: " + url)
            

            response = opener.open(url).read()

            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()

            # wait for 30 seconds
            time.sleep(30)
            continue


        # To handle exceptions
    except Exception as e:
        print(e)
