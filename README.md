# Log Anaysis

This project is for querying a large news article database and fetching the information.
It uses postgre and python

## Getting Started

Download the code with git clone https://github.com/mani11/udacity_log_analysis.git

### Prerequisites

**You should have python 3 installed.** 

_Download link_:https://www.python.org/downloads/

**You need VirtualBox tool to run VM.**

_Download Link_: https://www.virtualbox.org/wiki/Download_Old_Builds_5_2

**You need vagrant to configure the VM**

_Download Link_:https://www.vagrantup.com/downloads.html

Once you have the VMBox and vagrant you need to download the configuration for the VM

_Git link_: https://github.com/udacity/fullstack-nanodegree-vm

After the download,you will have a directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory:

**Start Virtual Machine:**
From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it.



You should create the following views:

1.This view is the join of articles and authors table. It has the information about the author id, author name, num of articles written by the author and the slug of the articles.

**CREATE view author_articles as SELECT a.author,a.slug,count(author) as num_of_articles,au.name FROM articles as a JOIN authors as au ON a.author = au.id group by author,a.slug,au.name;**

2.This view joins the above view _author_articles_ and _log table_ to give author name,articles written by them and the number of views for each article

**CREATE view popular_author as SELECT au_ar.slug,l.path,au_ar.name,count(*) as num FROM author_articles AS au_ar LEFT JOIN log AS l ON POSITION(au_ar.slug IN l.path)>0 where l.status='200 OK' group by au_ar.slug,l.path,au_ar.name order by au_ar.name;**

3.This view gives the total requests with a group by on date

**CREATE VIEW TOTAL_REQUESTS AS SELECT date(time),count(date(time)) as num FROM log GROUP BY date(time);**

4.This view gives the error requests group by date

**CREATE VIEW ERROR_REQUESTS AS SELECT date(time),count(date(time)) as err_requests FROM log WHERE status!='200 OK' GROUP BY date(time)**

5.This view gives the error rate on each date

**CREATE view ERROR_RATE AS SELECT a.date,a.num,e.err_requests,(CAST (e.err_requests AS DOUBLE PRECISION)/a.num)*100 as err_rate FROM TOTAL_REQUESTS a,ERROR_REQUESTS e WHERE a.date = e.date;**

### Usage
To run the code type the following command
python logAnalysis.py

_The Output will be in the same format as shown in the output file in the repository

## Authors

**Manleen Bhatia**


