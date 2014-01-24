#!/usr/bin/python2.7

import urllib2
import json
import argparse

bot_name = None
bot_text = None
bot_id = None
bot_url = None
bot_group = None
access_token = "INSERT_TOKEN_HERE"


def build_bot():
    global bot_id, bot_name, bot_url, bot_group

    print "Creating bot..."
    print bot_name
    print bot_url
    print "For group: "+bot_group

    data = {
        "bot" : {
            "name" : bot_name,
            "group_id" : bot_group,
            "avatar_url" : bot_url
        }
    }

    req = urllib2.Request("https://api.groupme.com/v3/bots?token="+access_token)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))


    data = json.load(response)


    bot_id = data["response"]["bot"]["bot_id"]

    print "Bot Id: " + bot_id

def run_bot():
    
    print "Posting " + bot_text + " From bot "+ bot_id

    """ Post from bot into group..
    """
    data = {
        "bot_id" : bot_id,
        "text" : bot_text
    }

    req = urllib2.Request("https://api.groupme.com/v3/bots/post?token="+access_token)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))

    print response.read()


parser = argparse.ArgumentParser(description="Create or Use Bot....must give bot_id or bot_name AND bot_url AND groupid.  Either way must supply text")

parser.add_argument("-t", "--text", dest="text",
                    help="text to send", metavar="TEXT")

parser.add_argument("-b", "--bot", dest="bot_id",
                    help="id of bot to reuse", metavar="bot_id")

parser.add_argument("-n", "--bot_name", dest="bot_name",
                    help="bot_name of bot to create", metavar="bot_name")

parser.add_argument("-u", "--bot_url", dest="bot_url",
                    help="bot_url of bot's image", metavar="bot_url")

parser.add_argument("-g", "--bot_group", dest="bot_group",
                    help="id of group for bot", metavar="bot_group")

args = parser.parse_args()
bot_text = args.text
bot_id = args.bot_id
bot_name = args.bot_name
bot_url = args.bot_url
bot_group = args.bot_group

if bot_text is not None:
    if bot_id is not None:
        run_bot()
    else:
        if bot_name is None or bot_url is None or bot_group is None:
            print "Please supply bot name AND url AND group id"
        else:
            build_bot()
            run_bot()
else:
    print "Error - please supply bot text"