#!/usr/bin/env python

# https://getpocket.com/@46bT2A86gc665p3fu9d744ed0xp5g576110y6cX119K9a5If964c9D3fh8eGz7e9

import json
import os
import sys
import urllib

POCKET_CONSUMER_KEY = os.environ['POCKET_CONSUMER_KEY']
POCKET_ACCESS_TOKEN = os.environ['POCKET_ACCESS_TOKEN']


def fetch(filename):
  data = urllib.urlencode({
    'consumer_key': POCKET_CONSUMER_KEY,
    'access_token': POCKET_ACCESS_TOKEN,
    'detailType': 'simple',
    'sort': 'newest',
    'state': 'archive',
  })
  urllib.urlretrieve('https://getpocket.com/v3/get?{}'.format(data), filename)

def save_to_json(html, filename):

  json.dumps(links, filename)

if __name__=='__main__':
  if len(sys.argv) < 2:
    raise ValueError("Missing parameters for [Pocket JSON file]")
  
  pocket_json_loc = sys.argv[1]
  fetch(pocket_json_loc)
