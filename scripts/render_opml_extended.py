#!/usr/bin/env python

import datetime
import operator
import os
import string
import sys
import time
import xml.etree.ElementTree as ET


def get_podcasts(filename):
  podcasts = []

  with open(filename) as i:
    parsed_xml = ET.fromstring(i.read())
    feed_xml = parsed_xml.find('.//outline[@text="feeds"]')

    for podcast_outline_xml in feed_xml.findall('outline'):
      for episode_outline in podcast_outline_xml.findall('outline[@userRecommendedDate]'):
        podcasts.append({
          'podcast_title': podcast_outline_xml.attrib['title'].encode('ascii', errors='xmlcharrefreplace'),
          'podcast_url': podcast_outline_xml.attrib['htmlUrl'],
          'episode_title': episode_outline.attrib['title'].encode('ascii', errors='xmlcharrefreplace'),
          'episode_url': episode_outline.attrib.get('overcastUrl', episode_outline.attrib['url']),
          'episode_user_update_date': episode_outline.attrib['userUpdatedDate'],
        })

  return sorted(podcasts, key=operator.itemgetter('episode_user_update_date'), reverse=True) 

def render_md(podcasts):
  lines = []
  def format_date(date_string):
    date_format = '%a %b %d %H:%M:%S %Y'
    date_string = date_string[:-6]
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").strftime('%b %d, %Y')

  for podcast in podcasts:
    lines.append('* [{}]({}) ([{}]({}))  '.format(podcast['episode_title'], podcast['episode_url'], podcast['podcast_title'], podcast['podcast_url']))
    lines.append('  {}'.format(format_date(podcast['episode_user_update_date'])))
    lines.append('')

  return '\n'.join(lines)

def render_template_to_file(template_loc, output_loc, vars):
  with open(template_loc, 'r') as i, open(output_loc, 'w') as o:
    t = string.Template(i.read())
    o.write(t.substitute(vars))

if __name__=='__main__':
  if len(sys.argv) < 4:
    raise ValueError("Missing parameters for [template file] [render file] [opml extended file location]")

  template_loc = sys.argv[1]
  render_loc = sys.argv[2]
  opml_file_loc = sys.argv[3]

  podcasts = get_podcasts(opml_file_loc)
  md = render_md(podcasts)
  render_template_to_file(template_loc, render_loc, {'podcasts': md})