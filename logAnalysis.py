import psycopg2
from datetime import datetime

DBNAME = 'news'

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# The popular_articles() method finds the popular articles of all time


def popular_articles():
    c.execute("SELECT a.title,count(*) as num FROM log as l join articles as a ON POSITION(a.slug IN l.path)>0 where l.status='200 OK'group by a.title order by num desc limit 3;")
    top_articles = c.fetchall()
    print("\nThe most popular 3 articles of all time are :")
    for article in top_articles:
        print('"' + article[0] + '" - ' + str(article[1]) + ' views')

# The popular_authors() method finds the popular authors based on the total views of the articles written by them


def popular_authors():
    c.execute("DROP VIEW popular_author;")
    c.execute("DROP VIEW author_articles;")
    c.execute("CREATE view author_articles as SELECT a.author,a.slug,count(author) as num_of_articles,au.name FROM articles as a JOIN authors as au ON a.author = au.id group by author,a.slug,au.name;")
    c.execute("CREATE view popular_author as SELECT au_ar.slug,l.path,au_ar.name,count(*) as num FROM author_articles AS au_ar LEFT JOIN log AS l ON POSITION(au_ar.slug IN l.path)>0 where l.status='200 OK' group by au_ar.slug,l.path,au_ar.name order by au_ar.name;")
    c.execute(
        "SELECT name ,SUM(num) FROM popular_author GROUP BY name order by sum desc;")
    top_authors = c.fetchall()
    print("\nThe popular authors of all time are : ")
    for author in top_authors:
        print(author[0] + ' - ' + str(author[1]) + ' views')

# The error_rate() method finds the days on which the percentage of failed requests is more than 1


def error_rate():
    c.execute("DROP VIEW ERROR_RATE;")
    c.execute("DROP VIEW TOTAL_REQUESTS;")
    c.execute("DROP VIEW ERROR_REQUESTS;")
    c.execute("CREATE VIEW TOTAL_REQUESTS AS SELECT date(time),count(date(time)) as num FROM log GROUP BY date(time);")
    c.execute("CREATE VIEW ERROR_REQUESTS AS SELECT date(time),count(date(time)) as err_requests FROM log WHERE status!='200 OK' GROUP BY date(time);")
    c.execute("CREATE view ERROR_RATE AS SELECT a.date,a.num,e.err_requests,(CAST (e.err_requests AS DOUBLE PRECISION)/a.num)*100 as err_rate FROM TOTAL_REQUESTS a,ERROR_REQUESTS e WHERE a.date = e.date;")
    c.execute("SELECT date,err_rate FROM ERROR_RATE WHERE err_rate>1;")
    err_rate = c.fetchall()
    print("\nMore than 1% of the requests result in error on the following days")
    for day in err_rate:
        print(datetime.strftime(
            day[0], '%b %d, %Y') + " - " + str(day[1]) + "%")


popular_articles()
popular_authors()
error_rate()
db.close()
