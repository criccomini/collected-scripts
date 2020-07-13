#!/usr/bin/env python

import datetime
import json
import string
import sys
import urllib
import urlparse

def get_links(filename):
  with open(filename) as i:
    parsed_json = json.load(i)
    links = parsed_json['list'].values()
    return sorted(links, key=lambda l: int(l['time_read']), reverse=True)

def render_md(links):
  lines = []
  last_month_entry = None

  def format_date(date_utc):
    return datetime.datetime.fromtimestamp(date_utc).strftime('%b %d, %Y')

  def format_month(date_utc):
    return datetime.datetime.fromtimestamp(date_utc).strftime('%B, %Y')

  def format_domain(url):
    return urlparse.urlparse(url).netloc

  for item_fields in links:
    title = item_fields.get('resolved_title', item_fields['given_title']).encode('ascii', errors='xmlcharrefreplace')
    url = item_fields.get('resolved_url', item_fields['given_url'])
    date = format_date(int(item_fields['time_read']))
    month = format_month(int(item_fields['time_read']))
    domain = format_domain(item_fields['resolved_url'])
    excerpt = item_fields['excerpt'].encode('ascii', errors='xmlcharrefreplace')

    if len(title) > 0 and len(url):
      if not last_month_entry or last_month_entry != month:
        last_month_entry = month
        lines.append('')
        lines.append('## {}'.format(month))
        lines.append('')

      lines.append('* {} [{}]({})  '.format(date, title, url))

  return '\n'.join(lines)

def render_template_to_file(template_loc, output_loc, vars):
  with open(template_loc, 'r') as i, open(output_loc, 'w') as o:
    t = string.Template(i.read())
    o.write(t.substitute(vars))

if __name__=='__main__':
  if len(sys.argv) < 4:
    raise ValueError("Missing parameters for [template file] [render file] [Pocket JSON file]")

  template_loc = sys.argv[1]
  render_loc = sys.argv[2]
  pocket_json_loc = sys.argv[3]
  links = get_links(pocket_json_loc)
  md = render_md(links)

  render_template_to_file(template_loc, render_loc, {'links': md})
