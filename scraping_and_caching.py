import requests
import json
from bs4 import BeautifulSoup
from dcts_and_class import *


CACHE_FNAME = "507_final_project_cache.json"
try:
    final_project_cache = open(CACHE_FNAME, "r")
    final_project_cache_read = final_project_cache.read()
    CACHE_DICTION = json.loads(final_project_cache_read)
    final_project_cache.close()
except:
    CACHE_DICTION = {}


# didn't end up using this function
def create_article_identifier_from_article_url(url_for_html):
    if url_for_html[-1] == "/":
        url_for_html = url_for_html[:-1]
    pre_title_slash_index = url_for_html.rfind("/")
    url_title_bit = url_for_html[pre_title_slash_index + 1:]
    article_identifier = url_title_bit
    return article_identifier

def get_html_of_last_jedi_article(article_to_html):
    article_url = article_to_html
    article_html = requests.get(article_url).text
    return article_html

# SOURCE: props to Anand for discovering the hack that informs this function
def get_star_wars_article_thumbnails_source_code(page_number=1):
    if page_number < 1 or type(page_number) != int:
        return "Please input an integer greater than zero\n"
    else:
        before_page_number = "http://ew.com/index.php?dispatch=people-tag-load-more-articles&pull_ads=1&page="
        the_page_number = str(page_number)
        after_page_number = "&current_author=null&current_tag=10567"
        ew_sw_pg_url = before_page_number + the_page_number + after_page_number
        ew_sw_pg_reqget = requests.get(ew_sw_pg_url).text
        ew_sw_pg = json.loads(ew_sw_pg_reqget)
        articles_list = []
        for article in ew_sw_pg:
            no_newlines = article.replace("\n", "")
            no_newlines_or_tabs = no_newlines.replace("\t", "")
            nice_html = no_newlines_or_tabs
            articles_list.append(nice_html)
        return articles_list

def get_star_wars_article_urls_from_one_page(page_number=1):  # TEASERS?
    article_thumbnails = get_star_wars_article_thumbnails_source_code(page_number)
    if article_thumbnails == "Please input an integer greater than zero\n":
        return article_thumbnails
    else:
        article_urls_one_page = []
        for article_thumbnail in article_thumbnails:
            aria_label_index = article_thumbnail.find("aria-label")
            first_quote_index = article_thumbnail.find('"', aria_label_index)
            value_start_index = first_quote_index + 1
            greater_than_index = article_thumbnail.find(">", aria_label_index)
            value_end_index = greater_than_index - 1
            article_type = article_thumbnail[value_start_index:value_end_index]
            if article_type == "video post type":  # filter out galleries
                href_index = article_thumbnail.rfind("href")  
                url_start = href_index + 6
                space_after_href_index = article_thumbnail.find(" ", href_index)
                url_end = space_after_href_index - 1
                url = article_thumbnail[url_start:url_end]
                # ADD TEASERS?
                #link_text_index = article_thumbnail.find(">", href_index) + 1
                #end_of_link_text_index = article_thumbnail.find("<", link_text_index)
                #teaser = article_thumbnail[link_text_index:end_of_link_text_index]
                article_urls_one_page.append(url)
        return article_urls_one_page

def get_star_wars_article_urls_from_multiple_pages(number_of_pages=5):
    test_of_number = get_star_wars_article_urls_from_one_page(number_of_pages)
    if test_of_number == "Please input an integer greater than zero\n":
        return test_of_number
    else:
        last_jedi_article_urls_multiple_pages = []
        for n in range(1, number_of_pages + 1):
            page_n_urls = get_star_wars_article_urls_from_one_page(n)
            for url in page_n_urls:
                last_jedi_article_urls_multiple_pages.append(url)
        return last_jedi_article_urls_multiple_pages

def cache_multiple_pages_of_last_jedi_articles(number_of_pages=5):  # SOURCE: 506_final_project.py
    urls_to_cache = get_star_wars_article_urls_from_multiple_pages(number_of_pages)
    for url in urls_to_cache:
        if url not in CACHE_DICTION:
            url_html = get_html_of_last_jedi_article(url)
            if "last-jedi" in url:
                CACHE_DICTION[url] = url_html.replace("\n", "")
            else:
                article_soup = BeautifulSoup(url_html, "html.parser")
                try:  # cf. http://ew.com/movies/2017/12/04/star-wars-bb-8-laura-dern/
                    article_keywords = article_soup.find("meta", {"name": "keywords"})["content"]
                    if "Last Jedi" in article_keywords:
                        CACHE_DICTION[url] = url_html.replace("\n", "")
                except:
                    pass
    outfile = open(CACHE_FNAME, "w")
    outfile.write(json.dumps(CACHE_DICTION))
    outfile.close()
    print("LAST JEDI ARTICLES CACHED")

def create_last_jedi_character_counts(article_instance):
    all_last_jedi_character_counts = {}
    for single_last_jedi_character in LAST_JEDI_CHARACTER_DCT:
        single_last_jedi_character_count_dct = {}
        about = 0
        for variant in LAST_JEDI_CHARACTER_DCT[single_last_jedi_character]:
            if article_instance.about(variant) is True:
                about = 1
                break  # exits for-loop, so need another for-loop for mentions
        mentions = 0
        for variant in LAST_JEDI_CHARACTER_DCT[single_last_jedi_character]:
            if about == 0 and article_instance.mentions(variant) is True:  # for my purposes, an article that's "about" a character can't "mention" them
                mentions = 1
                break
        single_last_jedi_character_count_dct["about"] = about
        single_last_jedi_character_count_dct["mentions"] = mentions
        all_last_jedi_character_counts[single_last_jedi_character] = single_last_jedi_character_count_dct
    return all_last_jedi_character_counts
