#!/usr/bin/env python

import cookielib
import os
import sys
import urllib
import urllib2

OVERCAST_EMAIL = os.environ['OVERCAST_EMAIL']
OVERCAST_PASSWORD = os.environ['OVERCAST_PASSWORD']

def login():
  # Set up cookie jar, so we can log in.
  cj = cookielib.CookieJar()
  cp = urllib2.HTTPCookieProcessor(cj)
  opener = urllib2.build_opener(cp)
  urllib2.install_opener(opener)
  data = urllib.urlencode({
    'email': OVERCAST_EMAIL,
    'password': OVERCAST_PASSWORD,
  })

  fetch('https://overcast.fm/login', data=data)
  
def fetch(url, filename=None, data=None):
  req = urllib2.Request(url, data)
  resp = urllib2.urlopen(req)
  contents = resp.read()
  if filename:
    with open(filename, "w") as o:
      o.write(contents)
  return contents

if __name__=='__main__':
  if len(sys.argv) < 2:
    raise ValueError("Missing parameters for [OPML file]")
  
  opml_file_loc = sys.argv[1]

  login()
  fetch('https://overcast.fm/account/export_opml/extended', filename=opml_file_loc)