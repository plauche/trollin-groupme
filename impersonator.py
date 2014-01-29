#!/usr/bin/python2.7

import urllib2
import urllib
import json
import argparse

from random import randint

bot_name = None
bot_text = None
bot_id = None
bot_url = None
bot_group = None
bot_msg = None
access_token = None


def select_member():
    """ Retrieve list of members in group...
    """
    global bot_name, bot_url, bot_group
    url = "https://api.groupme.com/v3/groups/"+bot_group+"?token="+access_token
    u = urllib.urlopen(url)
    data = json.load(u)
    names = []
    urls = []

    for i in data["response"]["members"]: 
        names.append(i["nickname"])
        urls.append(i["image_url"])

    y = randint(0,len(names)-1)
    bot_name = names[y] + " "
    bot_url = urls[y]


def get_group_info():
    url = "https://api.groupme.com/v3/groups?token="+access_token
    u = urllib.urlopen(url)


    data = json.load(u)

    for i in data["response"]:
        print i["group_id"]
        print i["name"]

def get_message():
    """ Retrieve list of members in group...
    """
    global bot_name, bot_url, bot_group, bot_msg
    url = "https://api.groupme.com/v3/groups/"+bot_group+"/messages?token="+access_token
    u = urllib.urlopen(url)

    data = json.load(u)

    index = randint(0, len(data["response"]["messages"]) - 1)

    bot_msg = data["response"]["messages"][index]["text"]
    bot_name = data["response"]["messages"][index]["name"] + " "
    bot_url = data["response"]["messages"][index]["avatar_url"]

def generate_bot():
    global bot_name, bot_url, bot_group, bot_msg

    print "-n \"%s\" -u \"%s\" -g \"%s\" -t \"%s\"" % (bot_name, bot_url, bot_group, bot_msg)


parser = argparse.ArgumentParser(description="Creates/uses a bot based off of someone in a given group.  Can also send duplicate messages")

parser.add_argument("-g", "--bot_group", dest="bot_group",
                    help="id of group for bot", metavar="bot_group")

parser.add_argument("-t", "--text", dest="text",
                    help="text to send", metavar="TEXT")

args = parser.parse_args()
bot_group = args.bot_group
bot_msg = args.text

with open('token.txt') as file:
    access_token = file.readline()

if access_token is not None:
    if bot_group is not None:
        
        # If we supply text then randomly pick a member...
        if bot_msg is not None:
            select_member()
        else:
        # Otherwise randomly pick an old message + that member
            get_message()

        generate_bot()
    else:
        print "Please supply group id"
else:
    print "Please supply access token in token.txt"