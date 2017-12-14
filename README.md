# SI 507 Fall 2017 Final Project

## BEFORE YOU DO ANYTHING ELSE:
This code relies on **[PostgreSQL](https://www.postgresql.org/) ("Postgres")**.  You will need to create a Postgres database on your computer in order for this code to run.  Once you have done so, add the name of the database (db\_name), the username you use to access
your database (db\_user, for me just my default computer user account), and
(if applicable) the password to your database (db\_password) to the file
**config\_example.py**.  Then change the name of that file to just **config.py**.
This code uses **Python 3**.

## WHAT THIS CODE DOES, IN BRIEF:
In anticipation of the release of *Star Wars: The Last Jedi*, *Entertainment
Weekly* has run [a series of preview articles](http://ew.com/star-wars/)
on their website.  I was curious how much coverage each of the "major"
characters in the movie got across all the textual articles (i.e. not the
articles consisting only of a photo gallery), so I wrote Python code to
scrape the site, count how many articles are "about" (i.e. mention in the title)
each character and how many "mention" (i.e. mention in the body but not in the
title) each character, store those counts in a Postgres database, and then
use that database to write an HTML file containing an easy-to-read table of the
results.  

## RUNNING THIS CODE:
Once you have Postgres installed and have your **config.py** file ready,
you need only open your command line, navigate to the right directory,
and run **SI507F17\_finalproject.py** by entering the following command:

`python3 SI507F17\_finalproject.py`

In your command line, the following statements should appear when you run
this code for the first time:

`LAST JEDI ARTICLES CACHED`

`HTML FILE WRITTEN`

Two files will be produced:

1. **507\_final\_project\_cache.json**: a JSON file of all the scraped HTML data

2. **SI507F17\_finalproject\_viz.html**: the aforementioned HTML visualization,
which is best viewed by opening it with a web browser

(You will see more alert statements in your terminal if you change the code
of some of the functions.  Also, if you try to run the code again without first
deleting the HTML file, a new one will not be written, and you will see the alert
`HTML FILE ALREADY EXISTS`.  It's no problem if you run the code again without
first deleting **507\_final\_project\_cache.json**; doing so will cache the HTML
of articles not cached the last time you ran it, either because the article is
new or because you asked for fewer pages of results.)

If you choose to run this code in a virtual environment, you should install
the modules in the file **requirements.txt** by activating your virtual
environment in the command line and then entering the following command:

`pip3 install -r requirements.txt`

(Again, this code was written in **Python 3**.)

If you want to run the tests I wrote for this code, I recommend first
opening **SI507F17\_finalproject.py** and changing the variable **running\_tests** from False to True.  This will prevent the code in this file from running interference on the test file.  Then navigate to the right directory in your command line and run **SI507F17\_finalproject\_tests.py** by entering the following command:

`python3 SI507F17_finalproject_tests.py`

Each test includes a message describing what the test is looking for, which
will appear if something goes wrong.

## FURTHER DETAILS ABOUT HOW THIS CODE WORKS:

The file **SI507F17\_finalproject.py** imports code from the following other files:

1. **config.py**, which contains database credentials

2. **dcts\_and\_class.py**, which contains the dictionaries of _Last Jedi_
characters that the code rules and defines a class of "EWArticle"

3. **scraping\_and\_caching.py**, which defines several functions used for
scraping and caching data from the _Entertainment Weekly_ site

4. **db\_functions.py**, which defines several functions used for making a
connection to the database and inserting the data

When **SI507F17\_finalproject.py** runs, it scrapes 15 pages (or however many
pages a user wishes to change it to on line 14) of _Entertainment Weekly_ article thumbnails (with a page corresponding to eight thumbnails when full), extracts the URLs of _Last Jedi_-related textual articles, and caches the HTML returned by those URLs in a JSON file.

For each article, the code uses the HTML to create an instance of the EWArticle class, which has methods to determine which characters it is "about" and "mentions."  As each article instance is thus evaluated, the global dictionary LAST\_JEDI\_CHARACTER\_COUNTS\_DCT is updated with the running counts of how many articles are about or mention each character.  

Once all the articles are done, the code sets up a database,
and the final counts in LAST\_JEDI\_CHARACTER\_COUNTS\_DCT are inserted into
two tables: "Abouts" (which details how many articles are about each character) and "Mentions" (which details how many articles mention each character).  

The two tables are then INNER JOIN-ed with PostgreSQL in order
for my HTML table to be written.

## CITATIONS OF BORROWED CODE:

* First of all, this project would never have worked if Anand Doshi hadn't
discovered the hack for obtaining the source code of as many article thumbnails as I desired, which my function get\_star\_wars\_article\_thumbnails\_source\_code() relies on.  
(See **scraping\_and\_caching.py**, lines 36-38.)

* Just about everything in **db_functions.py** is stolen from Jackie Cohen's
code of lecture 11 in SI 507 (Nov. 5, 2017).

* My function cache\_multiple\_pages\_of\_last\_jedi\_articles() (in
**scraping\_and\_caching.py**), minus the
BeautifulSoup (HTML parsing) bits, is adapted from caching code I used in my final project for SI 506 (Winter 2017), which means that I stole it from Jackie at some point.

* The BeautifulSoup bit of **SI507F17_finalproject.py** (lines 20-27) was
lifted from my code for this class's project 3, which in turn rips off Jackie's code from lecture 5 in SI 507 (Oct. 4, 2017).

* I only knew how to do the INNER JOIN in **SI507F17_finalproject.py** (line 41)
because Anand spent discussion section 11 of SI 507 (Nov. 6, 2017) teaching us PostgreSQL queries.

* Finally, it was Anand who suggested that the HTML table produced by my code include
pictures of the characters.
