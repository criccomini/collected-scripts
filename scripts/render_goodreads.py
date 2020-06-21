#!/usr/bin/env python

import datetime
import httplib
import string
import sys
import time
import urllib
import xml.etree.ElementTree as ET

def get_books(filename):
  books = []
  parsed_xml = ET.parse(filename)
  reviews_xml = parsed_xml.find('reviews')

  for review in reviews_xml.findall('review'):
    book = review.find('book')

    books.append({
      'title': book.find('title').text,
      'link': book.find('link').text,
      'started_at': review.find('started_at').text,
      'date_added': review.find('date_added').text,
      'read_at': review.find('read_at').text,
      'rating': int(review.find('rating').text),
    })

  return books

def render_md(books):
  lines = []
  def format_date(date_string):
    date_format = '%a %b %d %H:%M:%S %Y'
    date_string = date_string[:-11] + ' ' + date_string[-4:]
    return datetime.datetime.strptime(date_string, date_format).strftime('%b %d, %Y')

  for book in books:
    started_at = format_date(book['started_at']) if book['started_at'] else format_date(book['date_added'])
    read_at = 'Finished: {}'.format(format_date(book['read_at'])) if book['read_at'] else '**Currently Reading**'
    rating = '&middot; Rating: {}/5'.format(book['rating']) if book['rating'] else ''

    lines.append('* [{}]({})  '.format(book['title'], book['link']))
    lines.append('  Started: {} &middot; {}{}'.format(started_at, read_at, rating))
    lines.append('')

  return '\n'.join(lines)

def render_template_to_file(template_loc, output_loc, vars):
  with open(template_loc, 'r') as i, open(output_loc, 'w') as o:
    t = string.Template(i.read())
    o.write(t.substitute(vars))

if __name__=='__main__':
  if len(sys.argv) < 4:
    raise ValueError("Missing parameters for [template file] [render file] [Goodreads XML file]")

  template_loc = sys.argv[1]
  render_loc = sys.argv[2]
  goodreads_xml_loc = sys.argv[3]
  books = get_books(goodreads_xml_loc)
  md = render_md(books)

  render_template_to_file(template_loc, render_loc, {'books': md})
