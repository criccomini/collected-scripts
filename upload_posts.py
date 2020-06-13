#!/usr/bin/env python

import httplib
import json
import os
import sys

COLLECTED_NOTES_SITE_ID = os.environ['COLLECTED_NOTES_SITE_ID']
COLLECTED_NOTES_API_TOKEN = os.environ['COLLECTED_NOTES_API_TOKEN']
COLLECTED_NOTES_API_EMAIL = os.environ['COLLECTED_NOTES_API_EMAIL']

def put_file(post_id, markdown):
  conn = httplib.HTTPSConnection("collectednotes.com")
  headers = {
    'Authorization': '{} {}'.format(COLLECTED_NOTES_API_EMAIL, COLLECTED_NOTES_API_TOKEN),
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  }
  json_dict = {
    "note": 
    {
      "body": markdown, 
      "visibility": "public_site"
    }
  }
  url = '/sites/{}/notes/{}'.format(COLLECTED_NOTES_SITE_ID, post_id)
  conn.request("PUT", url, json.dumps(json_dict), headers)
  response = conn.getresponse()
  print 'post_id={}, URL={}, status={}, response={}'.format(post_id, url, response.status, response.reason)

if __name__=='__main__':
  if len(sys.argv) < 2:
    raise ValueError("Missing parameters for [render directory]")
  
  render_dir = sys.argv[1]

  for filename in os.listdir(render_dir):
    file_loc = os.path.join(render_dir, filename)

    if os.path.isfile(file_loc):
      with open(file_loc) as f:
        post_id = filename.split('.')[-2]
        put_file(post_id, f.read())
