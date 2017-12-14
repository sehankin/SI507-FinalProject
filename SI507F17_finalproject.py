from scraping_and_caching import *
from db_functions import *


# don't want this code to run when unittesting; set running_tests = True if so
running_tests = False
if running_tests == False:

    # this block of code relies on the imports from scraping_and_caching.py
    # it scrapes Entertainment Weekly's articles about The Last JEDI,
    # caches the articles' HTML in a JSON file,
    # and updates the dictionary LAST_JEDI_CHARACTER_COUNTS_DCT
    # with how many articles are "about" or "mention" each Last Jedi character
    cache_multiple_pages_of_last_jedi_articles(15)
    for url in CACHE_DICTION:  # SOURCE: project3_code.py
        # create article dictionary and instance
        article_dct = {}
        article_html = CACHE_DICTION[url]
        article_dct["url"] = url
        article_soup = BeautifulSoup(article_html, "html.parser")
        article_dct["title"] = article_soup.find("h1").text
        article_soup_author_text = article_soup.find("div", {"class": "author-text"})
        article_dct["author"] = article_soup_author_text.find("a").text
        article_soup_full_date = article_soup_author_text.find("div", {"class": "timestamp published-date padding-12-left"}).text.strip()
        article_dct["date"] = article_soup_full_date[:-16]
        article_dct["body"] = article_soup.find("div", {"id": "article-body"}).text.strip()
        article_inst = EWArticle(article_dct)
        # get character counts, add to LAST_JEDI_CHARACTER_COUNTS_DCT
        character_counts_in_article_inst = create_last_jedi_character_counts(article_inst)
        for character in character_counts_in_article_inst:
            LAST_JEDI_CHARACTER_COUNTS_DCT[character]["about"] += character_counts_in_article_inst[character]["about"]
            LAST_JEDI_CHARACTER_COUNTS_DCT[character]["mentions"] += character_counts_in_article_inst[character]["mentions"]


    # this block of code relies on the imports from db_functions.py
    # it inserts the data from LAST_JEDI_CHARACTER_COUNTS_DCT into two db tables,
    # then JOINs those two tables (SOURCE: section11_code.py)
    # to have all the data at hand for visualization
    setup_database()
    insert_character_counts_data_into_tables(LAST_JEDI_CHARACTER_COUNTS_DCT)
    joined_table = query_and_return("""SELECT * FROM Abouts INNER JOIN Mentions ON (Abouts.Character = Mentions.Character) ORDER BY Articles_About DESC, Articles_Mentioned DESC, Abouts.Character""")


    # this block of code relies on imported variables from dcts_and_class.py:
    # intro_paragraph, LAST_JEDI_CHARACTER_WOOKIEEPEDIA_LINK_DCT, and LAST_JEDI_CHARACTER_IMAGE_DCT
    # this block of code writes the data into an HTML table for visualization
    VIZ_FNAME = "SI507F17_finalproject_viz.html"
    try:
        viz_infile = open(VIZ_FNAME, "r")
        viz_infile.close()
        print("HTML FILE ALREADY EXISTS\n")
    except:
        viz_outfile = open(VIZ_FNAME, "w")
        viz_outfile.write("<!DOCTYPE html>\n")
        viz_outfile.write("<html>\n")
        viz_outfile.write("<head>\n")
        viz_outfile.write("\t<title>SI507 Final Project Data Viz</title>\n")
        viz_outfile.write("</head>\n")
        viz_outfile.write("<body>\n")
        viz_outfile.write("\t<h1>Data on <em>Entertainment Weekly</em>'s <em>Last Jedi</em> Articles</h1>\n")
        for line in intro_paragraph.split("\n"):
            viz_outfile.write("\t" + line + "\n")
        viz_outfile.write("\t<table border='1'>\n")
        viz_outfile.write("\t\t<tr id='header_row'>\n")
        viz_outfile.write("\t\t\t<th>Character</th>\n")
        viz_outfile.write("\t\t\t<th>Image</th>\n")
        viz_outfile.write("\t\t\t<th>Articles About</th>\n")
        viz_outfile.write("\t\t\t<th>Articles that Mention</th>\n")
        viz_outfile.write("\t\t</tr>\n")
        for row in joined_table:
            character = row["character"]
            articles_about = str(row["articles_about"])
            articles_mentioned = str(row["articles_mentioned"])
            wookieepedia_link = LAST_JEDI_CHARACTER_WOOKIEEPEDIA_LINK_DCT[character]
            img_src = LAST_JEDI_CHARACTER_IMAGE_DCT[character]
            viz_outfile.write("\t\t<tr id='" + character.lower() + "_row'>\n")
            viz_outfile.write("\t\t\t<td>" + "<a href='" + wookieepedia_link + "'>" + character + "</a></td>\n")
            viz_outfile.write("\t\t\t<td>" + "<img src='" + img_src + "' alt='" + character + "' height='300' width='225'></td>\n")
            viz_outfile.write("\t\t\t<td>" + articles_about + "</td>\n")
            viz_outfile.write("\t\t\t<td>" + articles_mentioned + "</td>\n")
            viz_outfile.write("\t\t</tr>\n")
        viz_outfile.write("\t</table>\n")
        viz_outfile.write("</body>\n")
        viz_outfile.write("</html>")
        viz_outfile.close()
        print("HTML FILE WRITTEN\n")
