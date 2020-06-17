#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import re
import sys
import urllib
import urllib2

GOODREADS_KEY = os.environ['GOODREADS_KEY']

def fetch(user_id, page):
  url = 'https://www.goodreads.com/review/list'
  headers = { 'Accept': 'text/xml' }
  params = urllib.urlencode({
    'v': 2,
    'id': user_id,
    'page': str(page),
    'per_page': str(20),
    'key': GOODREADS_KEY},
  )
  req = urllib2.Request(url, params, headers)
  resp = urllib2.urlopen(req)
  return resp.read()

def fetch_all(user_id, filename):
  page = 1
  goodreads_merged_xml = None

  while page:
    contents = fetch(user_id, page)

    # Merge page into complete list
    if goodreads_merged_xml is None:
      goodreads_merged_xml = ET.fromstring(contents)
    else:
      goodreads_page_xml = ET.fromstring(contents)
      reviews_xml = goodreads_page_xml.find('./reviews')
      goodreads_merged_xml.find('./reviews').extend(reviews_xml)

    # Fetch more pages?
    end, total = re.search('end="(\d+)" total="(\d+)"', contents).groups()
    page = page + 1 if end != total else None

  ET.ElementTree(goodreads_merged_xml).write(filename)

if __name__=='__main__':
  if len(sys.argv) < 3:
    raise ValueError("Missing parameters for [Goodreads XML file] [Goodreads user id]")
  
  goodreads_xml_loc = sys.argv[1]
  user_id = sys.argv[2]

  fetch_all(user_id, filename=goodreads_xml_loc)