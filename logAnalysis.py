#!/usr/bin/env python3
import psycopg2
from datetime import datetime

DBNAME = 'news'

try:
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
except psycopg2.Error as e:
    print(e)

# The popular_articles() method finds the popular articles of all time


def popular_articles():
    query_1 = (
        "SELECT a.title,count(*) as num FROM log as l "
        "join articles as a ON POSITION(a.slug IN l.path)>0 "
        "where l.status='200 OK'group by a.title order by num desc limit 3;")
    c.execute(query_1)
    top_articles = c.fetchall()
    print("\nThe most popular 3 articles of all time are :")
    for article in top_articles:
        print('"' + article[0] + '" - ' + str(article[1]) + ' views')

# The popular_authors() method finds the popular authors based
# on the total views of the articles written by them


def popular_authors():
    query_2 = (
        "SELECT name ,SUM(num) FROM popular_author "
        "GROUP BY name order by sum desc;")
    c.execute(query_2)
    top_authors = c.fetchall()
    print("\nThe popular authors of all time are : ")
    for author in top_authors:
        print(author[0] + ' - ' + str(author[1]) + ' views')

# The error_rate() method finds the days on which
# the percentage of failed requests is more than 1


def error_rate():
    query_3 = (
        "SELECT date,err_rate FROM ERROR_RATE WHERE err_rate>1;")
    c.execute(query_3)
    err_rate = c.fetchall()
    print("\nMore than 1% of the requests result"
          "in error on the following days")
    for day in err_rate:
        print(datetime.strftime(
            day[0], '%b %d, %Y') + " - " + str(day[1]) + "%")


popular_articles()
popular_authors()
error_rate()
db.close()
