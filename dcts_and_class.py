intro_paragraph = """
<p>
Welcome!  As we get closer to the release of <em>Star Wars: The Last Jedi</em>,
<em>Entertainment Weekly</em> has been running
<a href='http://ew.com/star-wars/'>a series of preview articles</a> about it.
I wrote a Python program to see how much each of the major characters
in the movie had written about them, the results of which are displayed below.
I investigated only textual articles, not photo galleries.
</p>
<p>
Each character has a row in the table below.  The "Articles About" column counts
how many <em>Entertainment Weekly</em> articles are "about" each character
(which I've defined as "the character is mentioned in the title").
The "Articles that Mention" column counts how many articles "mention" each character
(which I've defined as "the character is mentioned in the body of the article,
but not in the title").  The table is sorted in descending order of how many
articles each character has about them.
<p>
I've also included an "Image" column in case you're not sure who a character is.
(All images are taken from the character's page on
<a href='http://starwars.wikia.com/wiki/Main_Page'>Wookieepedia</a>, except
for the caretakers' image, which comes from <a href="http://za.ign.com/star-wars-1/109766/gallery/star-wars-the-last-jedi-latest-details?p=1">
this IGN page</a>.)  Additionally, each name in the "Character" column links
to the character's Wookieepedia page, but beware of <em>Last Jedi</em> spoilers
there!
</p>
<p>
I can't say I'm pleased that the porgs have the most articles about them.
</p>
"""

LAST_JEDI_CHARACTER_DCT = {
# http://starwars.wikia.com/wiki/Star_Wars:_Episode_VIII_The_Last_Jedi
"Luke": ["Luke Skywalker", "Luke", "Skywalker"],
"Leia": ["Leia Organa", "Leia", "Organa"],
"Han": ["Han Solo", "Han"],
"Kylo": ["Kylo Ren", "Kylo", "Ren", "Ben Solo"],
"Rey": ["Rey"],
"Finn": ["Finn", "FN-2187", "Eight-Seven"],
"Poe": ["Poe Dameron", "Poe", "Dameron"],
"Snoke": ["Snoke"],
"Maz": ["Maz Kanata", "Maz", "Kanata"],
"Hux": ["Armitage Hux", "Armitage", "Hux"],
"C-3PO": ["C-3PO", "3PO", "Threepio"],
"Phasma": ["Phasma"],
"Rose": ["Rose Tico", "Rose", "Tico"],
"Holdo": ["Amilyn Holdo", "Amilyn", "Holdo"],
"DJ": ["DJ"],
"Kaydel": ["Kaydel Ko Connix", "Kaydel", "Connix"],
"Chewie": ["Chewbacca", "Chewie"],
"Ackbar": ["Gial Ackbar", "Gial", "Ackbar"],
"Nunb": ["Nien Nunb", "Nien", "Nunb"],
"Plutt": ["Unkar Plutt", "Unkar", "Plutt"],
"R2-D2": ["R2-D2", "R2", "Artoo"],
"BB-8": ["BB-8"],
"BB-9E": ["BB-9E"],
"porgs": ["porg", "porgs", "Porg", "Porgs"],
"vulptices": ["vulptex", "vulptices", "Vulptex", "Vulptices", "crystal fox", "crystal foxes"],
"caretakers": ["caretaker", "caretakers"]
}

LAST_JEDI_CHARACTER_COUNTS_DCT = {
# "about" means "mentioned in the title of the article"
# "mentions" means "not mentioned in the title of the article, but in its body"
"Luke": {"about": 0, "mentions": 0},
"Leia": {"about": 0, "mentions": 0},
"Han": {"about": 0, "mentions": 0},
"Kylo": {"about": 0, "mentions": 0},
"Rey": {"about": 0, "mentions": 0},
"Finn": {"about": 0, "mentions": 0},
"Poe": {"about": 0, "mentions": 0},
"Snoke": {"about": 0, "mentions": 0},
"Maz": {"about": 0, "mentions": 0},
"Hux": {"about": 0, "mentions": 0},
"C-3PO": {"about": 0, "mentions": 0},
"Phasma": {"about": 0, "mentions": 0},
"Rose": {"about": 0, "mentions": 0},
"Holdo": {"about": 0, "mentions": 0},
"DJ": {"about": 0, "mentions": 0},
"Kaydel": {"about": 0, "mentions": 0},
"Chewie": {"about": 0, "mentions": 0},
"Ackbar": {"about": 0, "mentions": 0},
"Nunb": {"about": 0, "mentions": 0},
"Plutt": {"about": 0, "mentions": 0},
"R2-D2": {"about": 0, "mentions": 0},
"BB-8": {"about": 0, "mentions": 0},
"BB-9E": {"about": 0, "mentions": 0},
"porgs": {"about": 0, "mentions": 0},
"vulptices": {"about": 0, "mentions": 0},
"caretakers": {"about": 0, "mentions": 0}
}

LAST_JEDI_CHARACTER_WOOKIEEPEDIA_LINK_DCT = {
# URLs for their Wookieepedia articles
"Luke": "http://starwars.wikia.com/wiki/Luke_Skywalker",
"Leia": "http://starwars.wikia.com/wiki/Leia_Organa",
"Han": "http://starwars.wikia.com/wiki/Han_Solo",
"Kylo": "http://starwars.wikia.com/wiki/Kylo_Ren",
"Rey": "http://starwars.wikia.com/wiki/Rey",
"Finn": "http://starwars.wikia.com/wiki/Finn",
"Poe": "http://starwars.wikia.com/wiki/Poe_Dameron",
"Snoke": "http://starwars.wikia.com/wiki/Snoke",
"Maz": "http://starwars.wikia.com/wiki/Maz_Kanata",
"Hux": "http://starwars.wikia.com/wiki/Armitage_Hux",
"C-3PO": "http://starwars.wikia.com/wiki/C-3PO",
"Phasma": "http://starwars.wikia.com/wiki/Phasma",
"Rose": "http://starwars.wikia.com/wiki/Rose_Tico",
"Holdo": "http://starwars.wikia.com/wiki/Amilyn_Holdo",
"DJ": "http://starwars.wikia.com/wiki/DJ",
"Kaydel": "http://starwars.wikia.com/wiki/Kaydel_Ko_Connix",
"Chewie": "http://starwars.wikia.com/wiki/Chewbacca",
"Ackbar": "http://starwars.wikia.com/wiki/Gial_Ackbar",
"Nunb": "http://starwars.wikia.com/wiki/Nien_Nunb",
"Plutt": "http://starwars.wikia.com/wiki/Unkar_Plutt",
"R2-D2": "http://starwars.wikia.com/wiki/R2-D2",
"BB-8": "http://starwars.wikia.com/wiki/BB-8",
"BB-9E": "http://starwars.wikia.com/wiki/BB-9E",
"porgs": "http://starwars.wikia.com/wiki/Porg",
"vulptices": "http://starwars.wikia.com/wiki/Vulptex",
"caretakers": "http://starwars.wikia.com/wiki/Caretakers"
}

LAST_JEDI_CHARACTER_IMAGE_DCT = {
# URLs for character pictures
"Luke": "https://vignette.wikia.nocookie.net/starwars/images/2/20/LukeTLJ.jpg/revision/latest?cb=20170927034529",
"Leia": "https://vignette.wikia.nocookie.net/starwars/images/a/ab/General_Leia_Organa_SWCT.png/revision/latest?cb=20170718232129",
"Han": "https://vignette.wikia.nocookie.net/starwars/images/e/e2/TFAHanSolo.png/revision/latest?cb=20160208055002",
"Kylo": "https://vignette.wikia.nocookie.net/starwars/images/6/60/KyloRenTLJEntertainmentWeekly.jpg/revision/latest?cb=20170919232026",
"Rey": "https://vignette.wikia.nocookie.net/starwars/images/f/f8/ReyTLJEntertainmentWeeklyNovember.png/revision/latest?cb=20171119211748",
"Finn": "https://vignette.wikia.nocookie.net/starwars/images/2/2e/Finn_EW.png/revision/latest?cb=20171114012257",
"Poe": "https://vignette.wikia.nocookie.net/starwars/images/7/74/PoeDameronTLJEW.png/revision/latest?cb=20171107005134",
"Snoke": "https://vignette.wikia.nocookie.net/starwars/images/9/9d/SnokeTLJ.png/revision/latest?cb=20170910213521",
"Maz": "https://vignette.wikia.nocookie.net/starwars/images/e/e6/Maz_Kanata_HS.png/revision/latest?cb=20171111230137",
"Hux": "https://vignette.wikia.nocookie.net/starwars/images/2/2c/HuxTLJPromo_%28no_background%29.png/revision/latest?cb=20171119220230",
"C-3PO": "https://vignette.wikia.nocookie.net/starwars/images/7/7e/ThreepioTFA-Fathead.png/revision/latest?cb=20161109035240",
"Phasma": "https://vignette.wikia.nocookie.net/starwars/images/e/e7/PhasmaHS-Fathead.png/revision/latest?cb=20161003052605",
"Rose": "https://vignette.wikia.nocookie.net/starwars/images/c/c6/Rose_Tico_EW.png/revision/latest?cb=20171105220620",
"Holdo": "https://vignette.wikia.nocookie.net/starwars/images/a/a4/Holdo-Elle.png/revision/latest?cb=20171205174318",
"DJ": "https://vignette.wikia.nocookie.net/starwars/images/a/a4/Holdo-Elle.png/revision/latest?cb=20171205174318",
"Kaydel": "https://vignette.wikia.nocookie.net/starwars/images/5/52/BillieLourd1.jpg/revision/latest?cb=20171005194617",
"Chewie": "https://vignette.wikia.nocookie.net/starwars/images/4/4f/Chewbacca-TFA.png/revision/latest?cb=20160106141736",
"Ackbar": "https://vignette.wikia.nocookie.net/starwars/images/2/29/Admiral_Ackbar_RH.png/revision/latest?cb=20170907053204",
"Nunb": "https://vignette.wikia.nocookie.net/starwars/images/1/14/Old_nien_nunb_-_profile.png/revision/latest?cb=20160813010804",
"Plutt": "https://vignette.wikia.nocookie.net/starwars/images/b/b7/Unkar_Plutt-RO_U_Visual_Guide.png/revision/latest?cb=20170119072240",
"R2-D2": "https://vignette.wikia.nocookie.net/starwars/images/e/eb/ArtooTFA2-Fathead.png/revision/latest?cb=20161108040914",
"BB-8": "https://vignette.wikia.nocookie.net/starwars/images/6/68/BB8-Fathead.png/revision/latest?cb=20161108050455",
"BB-9E": "https://vignette.wikia.nocookie.net/starwars/images/0/05/BB-9E_Fathead.png/revision/latest?cb=20170902001319",
"porgs": "https://vignette.wikia.nocookie.net/starwars/images/2/2e/Porg.png/revision/latest?cb=20170721231437",
"vulptices": "https://vignette.wikia.nocookie.net/starwars/images/f/fb/Vulptex_2.png/revision/latest?cb=20171121062844",
#"caretakers": "https://vignette.wikia.nocookie.net/starwars/images/1/1e/Caretakers.jpg/revision/latest?cb=20170820214831"
"caretakers": "http://sm.ign.com/t/ign_za/screenshot/b/ba-hrefhtt/ba-hrefhttpewcommovies20170809star-wars-last-jedi-porgs-care_6esn.640.jpg"
}


class EWArticle():
    def __init__(self, article_dct={}):
        self.url = article_dct["url"]
        self.title = article_dct["title"]
        self.author = article_dct["author"]
        self.date = article_dct["date"]
        self.body = article_dct["body"]

    def __str__(self):
        return self.title + " (" + self.url + ")"

    def __repr__(self):
        return self.title + " (" + self.url + "), " + self.date

    def __contains__(self, input_str):
        return input_str in self.title or input_str in self.body

    def about(self, input_str):
        return input_str in self.title

    def mentions(self, input_str):
        return input_str in self.body
