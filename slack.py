#!/usr/bin/env python3
# 
# 
# DATAMA SAS
# 
# Copyright (c) [2022] DataMa SAS, All Rights Reserved.
# 
# Notice created by Django <django@datama.fr>
# Contributors : Django <django@datama.fr>, Wazhabits <anatole@datama.fr>
# __________________
# 
# NOTICE:  All information contained herein is, and remains
# the property of DataMa SAS and/or some open source packages used 
# if any.  The intellectual and technical concepts contained
# herein are proprietary to DataMa SAS 
# and its suppliers and may be covered by French and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from DataMa SAS.
# __________________
# 

import os
import requests
import json
import argparse
import sys
 
parser = argparse.ArgumentParser(description="Just an example",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--user", required=False, help="User name")
parser.add_argument("-i", "--impact", help="Impact")
parser.add_argument("-c", "--commit-url", help="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/commit/GITHUB_SHA")
parser.add_argument("-p", "--pull-request-url", help="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/pull/$github.event.number")
parser.add_argument("-w", "--web-hook", required=True, help="Webhook url")
parser.add_argument("-s", "--status", default="failure", choices=['failure', 'cancelled', 'success'], help="Status")
parser.add_argument("-k", "--scope", default="staging", choices=['staging', 'prod', 'temporary'], help="Scope")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
parser.add_argument("action", help="Action message")

GITHUB_AVATAR_SERVER_URL = "https://avatars.githubusercontent.com"
# GITHUB_SERVER_URL = os.getenv("GITHUB_SERVER_URL")
# GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
# GITHUB_ACTOR = os.getenv("GITHUB_ACTOR","DataMa-Solutions")


args = parser.parse_args()
config = vars(args)
print(config)
WEBHOOK_URL = config.get("web_hook") #"https://hooks.slack.com/services/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"
USER = config.get("user","DataMa-Solutions")
if(USER is None):
	USER = "DataMa-Solutions"
ACTION = config.get("action","Building latest changes")
IMPACT = config.get("impact")
SCOPE = config.get("scope","staging")
STATUS_CODE = config.get("status","failure")
COMMIT_URL = config.get("commit_url",None)
PR_URL = config.get("pull-request-url",None)
if(IMPACT is None):
	IMPACT = "None"
STATUS = ":x:"
if(STATUS_CODE == "cancelled"):
	STATUS = ":large_orange_circle:"
if(STATUS_CODE == "success"):
	STATUS = ":launched:"

IMG_URL = "{}/{}?size=50".format(GITHUB_AVATAR_SERVER_URL,USER)

payload = {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":rocket: Auto Build notification",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": " *Action:* {0}\n*Impact*: {1} \n*Scope:* {2}\n*Status:* {3} _(By {4})_".format(ACTION,IMPACT,SCOPE,STATUS,USER)
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "image",
					"image_url": IMG_URL,
					"alt_text": "{}".format(USER)
				},
				{
					"type": "plain_text",
					"text": "Launched by {}".format(USER),
					"emoji": True
				}
			]
		},
		# {
		# 	"type": "actions",
		# 	"elements": [
		# 		{
		# 			"type": "button",
		# 			"text": {
		# 				"type": "plain_text",
		# 				"text": "Open Pull request",
		# 				"emoji": True
		# 			},
		# 			"style": "primary",
		# 			"value": "done"
		# 		},
		# 		{
		# 			"type": "button",
		# 			"text": {
		# 				"type": "plain_text",
		# 				"text": "Stop build",
		# 				"emoji": True
		# 			},
		# 			"value": "default"
		# 		},
		# 		{
		# 			"type": "button",
		# 			"text": {
		# 				"type": "plain_text",
		# 				"text": ":x: Stop build",
		# 				"emoji": True
		# 			},
		# 			"style": "danger",
		# 			"value": "failed"
		# 		}
		# 	]
		# }
	]
}

if(PR_URL is not None and PR_URL != 'None'):
	payload["blocks"][1]["accessory"] = {
		"type": "button",
		"text": {
			"type": "plain_text",
			"text": "Open Pull Request :point_right:",
			"emoji": True
		},
		"value": "open_pr",
		"url": PR_URL,
		"action_id": "button-action"
	}
if(COMMIT_URL is not None and COMMIT_URL != 'None'):
	payload["blocks"][1]["accessory"] = {
		"type": "button",
		"text": {
			"type": "plain_text",
			"text": ":eyes: Open commit",
			"emoji": True
		},
		"value": "open_commit",
		"url": COMMIT_URL,
		"action_id": "button-action"
	}
result = requests.post(WEBHOOK_URL,json.dumps(payload)).json()