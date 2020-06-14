#!/usr/bin/env python

"""
<?xml version="1.0" encoding="UTF-8"?>
<GoodreadsResponse>
    <reviews start="1" end="20" total="67">
        <review>
            <id>3385849648</id>
            <book>
                <id type="integer">18757378</id>
                <isbn nil="true"/>
                <isbn13 nil="true"/>
                <text_reviews_count type="integer">82</text_reviews_count>
                <uri>kca://book/amzn1.gr.book.v1.QM6xKkNdZPzk3KX-d6TWVg</uri>
                <title>The Plague</title>
                <title_without_series>The Plague</title_without_series>
                <image_url>https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1481459910l/18757378._SX98_.jpg</image_url>
                <small_image_url>https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1481459910l/18757378._SY75_.jpg</small_image_url>
                <large_image_url/>
                <link>https://www.goodreads.com/book/show/18757378-the-plague</link>
                <num_pages></num_pages>
                <format></format>
                <edition_information/>
                <publisher></publisher>
                <publication_day></publication_day>
                <publication_year></publication_year>
                <publication_month></publication_month>
                <average_rating>4.00</average_rating>
                <ratings_count>157789</ratings_count>
                <description>A haunting tale of human resilience in the face of unrelieved horror, Camus' novel about a bubonic plague ravaging the people of a North African coastal town is a classic of twentieth-century literature.</description>
                <authors>
                    <author>
                        <id>957894</id>
                        <name>Albert Camus</name>
                        <role></role>
                        <image_url nophoto='false'>
                            <![CDATA[https://images.gr-assets.com/authors/1506091612p5/957894.jpg]]>
                        </image_url>
                        <small_image_url nophoto='false'>
                            <![CDATA[https://images.gr-assets.com/authors/1506091612p2/957894.jpg]]>
                        </small_image_url>
                        <link>
                            <![CDATA[https://www.goodreads.com/author/show/957894.Albert_Camus]]>
                        </link>
                        <average_rating>4.00</average_rating>
                        <ratings_count>1047147</ratings_count>
                        <text_reviews_count>39654</text_reviews_count>
                    </author>
                </authors>
                <published></published>
                <work>
                    <id>2058116</id>
                    <uri>kca://work/amzn1.gr.work.v1.N9zg-IR-oaLlDKsk5yOm3A</uri>
                </work>
            </book>
            <rating>0</rating>
            <votes>0</votes>
            <spoiler_flag>false</spoiler_flag>
            <spoilers_state>none</spoilers_state>
            <shelves>
                <shelf exclusive='true' id='128165999' name='currently-reading' review_shelf_id='3025257009' sortable='false'></shelf>
            </shelves>
            <recommended_for></recommended_for>
            <recommended_by></recommended_by>
            <started_at>Wed Jun 10 21:44:29 -0700 2020</started_at>
            <read_at></read_at>
            <date_added>Wed Jun 10 21:44:29 -0700 2020</date_added>
            <date_updated>Fri Jun 12 22:53:17 -0700 2020</date_updated>
            <read_count>1</read_count>
            <body></body>
            <comments_count>0</comments_count>
            <url>
                <![CDATA[https://www.goodreads.com/review/show/3385849648]]>
            </url>
            <link>
                <![CDATA[https://www.goodreads.com/review/show/3385849648]]>
            </link>
            <owned>0</owned>
        </review>
"""

import datetime
import httplib
import os
import string
import sys
import time
import urllib
import xml.etree.ElementTree as ET

GOODREADS_KEY = os.environ['GOODREADS_KEY']

def fetch_page(user_id, page):
  conn = httplib.HTTPSConnection("www.goodreads.com")
  headers = { 'Accept': 'text/xml' }
  params = urllib.urlencode({
    'v': 2,
    'id': user_id,
    'page': str(page),
    'per_page': str(100),
    'key': GOODREADS_KEY},
  )
  url = '/review/list?' + params
  conn.request("GET", url, params, headers)
  response = conn.getresponse()
  return response.read()

def get_books(user_id):
  page = 0
  books = []
  end, total = -2, -1

  while end < total:
    page += 1
    parsed_xml = ET.fromstring(fetch_page(user_id, page))

    # Update end and total for next loop
    reviews_xml = parsed_xml.find('reviews')
    end = reviews_xml.attrib['end']
    total = reviews_xml.attrib['total']

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
    rating = '; Rating: {}/5'.format(book['rating']) if book['rating'] else ''

    lines.append('* [{}]({})  '.format(book['title'], book['link']))
    lines.append('  Started: {}; {}{}'.format(started_at, read_at, rating))

  return '\n'.join(lines)

def render_template_to_file(template_loc, output_loc, vars):
  with open(template_loc, 'r') as i, open(output_loc, 'w') as o:
    t = string.Template(i.read())
    o.write(t.substitute(vars))

if __name__=='__main__':
  if len(sys.argv) < 4:
    raise ValueError("Missing parameters for [template file] [render file] [goodreads user id]")

  template_loc = sys.argv[1]
  render_loc = sys.argv[2]
  user_id = sys.argv[3]
  books = get_books(user_id)
  md = render_md(books)

  render_template_to_file(template_loc, render_loc, {'books': md})
