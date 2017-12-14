import unittest
from SI507F17_finalproject import *


class TestScrapingAndCaching(unittest.TestCase):
    def setUp(self):
        self.thumbnails = get_star_wars_article_thumbnails_source_code()
        self.urls_one_page = get_star_wars_article_urls_from_one_page()
        self.urls_multiple_pages = get_star_wars_article_urls_from_multiple_pages()
        self.caching = cache_multiple_pages_of_last_jedi_articles()

    def test_of_get_star_wars_article_thumbnails_source_code(self):
        self.assertEqual(type(self.thumbnails), list, "Testing that the function get_star_wars_article_thumbnails_source_code() returns a list")
        for thumbnail in self.thumbnails:
            self.assertEqual(thumbnail[:8], "<article", "Testing that the function get_star_wars_article_thumbnails_source_code returns article thumbnail source code")

    def test_of_get_last_jedi_article_urls_from_one_page(self):
        self.assertEqual(type(self.urls_one_page), list, "Testing that the function get_last_jedi_article_urls_from_one_page() returns a list")
        for url in self.urls_one_page:
            self.assertEqual(url[:7], "http://", "Testing that the function get_last_jedi_article_urls_from_one_page() returns a list of URLs")

    def test_of_get_last_jedi_article_urls_from_multiple_pages(self):
        self.assertEqual(type(self.urls_multiple_pages), list, "Testing that the function get_last_jedi_article_urls_from_multiple_pages() returns a list")
        self.assertTrue(len(self.urls_multiple_pages) > len(self.urls_one_page), "Testing that with no number of pages passed in, the function test_of_get_last_jedi_article_urls_from_multiple_pages() returns multiple pages")
        for url in self.urls_multiple_pages:
            self.assertEqual(url[:7], "http://", "Testing that the function get_last_jedi_article_urls_from_multiple_pages() returns a list of URLs")

    def test_of_cache_multiple_pages_of_last_jedi_articles(self):
        for key in CACHE_DICTION:
            self.assertEqual(key[:7], "http://", "Testing that the function test_of_cache_multiple_pages_of_last_jedi_articles() makes URLs keys")
            self.assertTrue("<html" in CACHE_DICTION[key], "Testing that the function test_of_cache_multiple_pages_of_last_jedi_articles() makes articles' HTML values")


class TestClassAndCounts(unittest.TestCase):
    def setUp(self):
        self.snoke_article_dct = {}
        self.snoke_article_dct["url"] = "http://ew.com/movies/2017/11/22/star-wars-last-jedi-andy-serkis-snoke-backstory/"
        self.snoke_article_html = get_html_of_last_jedi_article(self.snoke_article_dct["url"])
        self.snoke_article_soup = BeautifulSoup(self.snoke_article_html, "html.parser")
        self.snoke_article_dct["title"] = self.snoke_article_soup.find("h1").text
        self.snoke_article_soup_author_text = self.snoke_article_soup.find("div", {"class": "author-text"})
        self.snoke_article_dct["author"] = self.snoke_article_soup_author_text.find("a").text
        self.snoke_article_soup_full_date = self.snoke_article_soup_author_text.find("div", {"class": "timestamp published-date padding-12-left"}).text.strip()
        self.snoke_article_dct["date"] = self.snoke_article_soup_full_date[:-16]
        self.snoke_article_dct["body"] = self.snoke_article_soup.find("div", {"id": "article-body"}).text.strip()
        self.snoke_article_instance = EWArticle(self.snoke_article_dct)
        self.counts = create_last_jedi_character_counts(self.snoke_article_instance)

    def test_of_ew_article_class(self):  # fetches an article directly from EW because who knows what ends up in CACHE_DICTION/self.caching
        self.assertEqual(self.snoke_article_instance.url, "http://ew.com/movies/2017/11/22/star-wars-last-jedi-andy-serkis-snoke-backstory/", "Testing that an EWArticle instance's self.url is the article's URL")
        self.assertTrue("Andy Serkis says pain and greed drive Supreme Leader Snoke in" in self.snoke_article_instance.title, "Testing that an EWArticle instance's self.title is approximately the title of the article (save for stupid HTML entities)")
        self.assertEqual(self.snoke_article_instance.author, "Anthony Breznican", "Testing that an EWArticle instances's self.author is the article's author")
        self.assertEqual(self.snoke_article_instance.date, "November 22, 2017", "Testing that an EWArticle instance's self.date is the article's date, without the time")
        self.assertTrue("Some people absorb unspeakable pain" in self.snoke_article_instance.body, "Testing that an EWArticle instance's self.body is the article's body")
        self.assertTrue(self.snoke_article_instance.title in self.snoke_article_instance.__str__() and self.snoke_article_instance.url in self.snoke_article_instance.__str__(), "Testing EWArticle class's __str__() method")
        self.assertTrue(self.snoke_article_instance.title in self.snoke_article_instance.__repr__() and self.snoke_article_instance.url in self.snoke_article_instance.__repr__() and self.snoke_article_instance.date in self.snoke_article_instance.__repr__(), "Testing EWArticle class's __repr__() method")
        self.assertEqual(self.snoke_article_instance.__contains__("Snoke"), True, "Testing EWArticle class's __contains__() method in a case that should be True")
        self.assertEqual(self.snoke_article_instance.__contains__("potato"), False, "Testing EWArticle class's __contains__() method in a case that should be False")
        self.assertEqual(self.snoke_article_instance.about("Snoke"), True, "Testing EWArticle class's about() method in a case that should be True")
        self.assertEqual(self.snoke_article_instance.about("Luke"), False, "Testing EWArticle class's about() method in a case that should be False")
        self.assertEqual(self.snoke_article_instance.mentions("Luke"), True, "Testing EWArticle class's mentions() method in a case that should be True")
        self.assertEqual(self.snoke_article_instance.mentions("BB-8"), False, "Testing EWArticle class's mentions() method in a case that should be False")

    def test_of_create_last_jedi_character_counts(self):
        self.assertEqual(self.counts["Snoke"]["about"], 1, "Testing that the function create_last_jedi_character_counts() assigns characters mentioned in an EWArticle instance's self.title {'about': 1}")
        self.assertEqual(self.counts["Luke"]["about"], 0, "Testing that the function create_last_jedi_character_counts() assigns characters not mentioned in an EWArticle instance's self.title {'about': 0}")
        self.assertEqual(self.counts["BB-8"]["mentions"], 0, "Testing that the function create_last_jedi_character_counts() assigns characters not mentioned in an EWArticle instance's self.body {'mentions': 0}")
        self.assertEqual(self.counts["Luke"]["mentions"], 1, "Testing that the function create_last_jedi_character_counts() assigns characters mentioned in an EWArticle instance's self.body {'mentions': 1}")
        self.assertEqual(self.counts["Snoke"]["mentions"], 0, "Testing that the function create_last_jedi_character_counts() assigns characters mentioned in an EWArticle instance's self.title and self.body {'mentions': 0}")


class TestDatabase(unittest.TestCase):
    def test_of_abouts_table(self):
        for character in LAST_JEDI_CHARACTER_DCT:
            self.abouts_test = query_and_return("SELECT * FROM Abouts WHERE Character = '" + character + "'")
            self.assertTrue("id" in self.abouts_test[0] and "character" in self.abouts_test[0] and "articles_about" in self.abouts_test[0], "Testing that every character was inserted into the Abouts table")

    def test_of_mentions_table(self):
        for character in LAST_JEDI_CHARACTER_DCT:
            self.mentions_test = query_and_return("SELECT * FROM Mentions WHERE Character = '" + character + "'")
            self.assertTrue("id" in self.mentions_test[0] and "character" in self.mentions_test[0] and "articles_mentioned" in self.mentions_test[0], "Testing that every character was inserted into the Mentions table")


# I decided not to test my HTML file output because unlike the tests above,
# such a test would be laborious to do without actually running my main code.
# Furthermore, since the point of the HTML file is to be a visualization,
# it makes more sense to just look at it to "test" how it turned out.


if __name__ == '__main__':
    unittest.main(verbosity=2)
