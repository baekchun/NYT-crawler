import argparse
import logging

from translate import Translate
from selenium import webdriver


# log all the URLs that I was unable to crawl
logging.basicConfig(filename='error_URLs.log')

# only log the WARNING logs from Selenium
logging.getLogger("selenium").setLevel(logging.WARNING)


class Crawler:
    """
    Crawler object that visits different pages on New York Times
    """
    def __init__(self):
        self.browser = webdriver.Chrome('/Users/baekchunkim/Downloads/chromedriver')

    def getBrowser(self):
        return self.browser


class LinkScraper(Crawler):

    def __init__(self, options):
        # initialize a cralwer object for Link Scraper
        super(LinkScraper, self).__init__()
        self.crawler = self.browser

        # initial URL to NYC international articles homepage
        self.URL = "https://cn.nytimes.com/world/{PAGE_NUM}/"

        # scrape up to this page number
        self.MAX_PAGE_NUM = int(options.num_pages)

        # start scraping from page 1
        self.page_num = 1

        # File number is incremented by one
        self.FILE_NUM = 0

    def getLinks(self):
        """
        Extracts links to articles from a NYT International news page
        """

        # get the webpage
        self.crawler.get(
            self.URL.format(
                PAGE_NUM=self.page_num
            )
        )

        # extract the aritcle links 
        links = self.crawler.find_elements_by_css_selector("div.basic-list h3 > a")
        
        # increment the page number
        self.page_num += 1

        # return just the links, not the WebElements
        return [link.get_attribute("href") for link in links]

    def scrape(self):
        """
        Let the Scraping Begin!
        """

        # create a scraper object
        scraper = ArticleScraper()

        # scrape up to x pages on NYT
        for i in range(self.MAX_PAGE_NUM):

            # extract all links to articles on this page
            links = self.getLinks()

            # for each article link, go into it and extract content
            for url in links[:2]:        
                bi_text = scraper.extract(url)
        
                # write to file
                self.write(bi_text)

    def write(self, text):
        """
        Write bitext article to a txt file
        input: text - a tuple of English text, Chinese text and translated text
        from Chinese to English
        """

        if text:

            # Set the filename
            template = "output__{NUM}.txt"
            filename = template.format(
                NUM=format(self.FILE_NUM, "03") # pad with 3 zeros in front
            )

            with open(filename, 'w') as output:
                # text is a tuple of en, ch and translated sentences 
                for t in text:
                    for sentence in t:
                        output.write(sentence + "\n")
                
                    # separate by asterisks
                    output.write("************************************************************" + "\n")
    
            # increment the file number
            self.FILE_NUM += 1

class ArticleScraper(Crawler):

    def __init__(self):
        # initialize crawler object for Article Scraper
        super(ArticleScraper, self).__init__()
        self.crawler = self.browser

        # initialize a translator object 
        self.translator = Translate()

        self.CSS_SELECTOR = "div.bilingual.cf > div.cf.articleContent"

    def extract(self, url):
        """
        For each article, separate the chinese and english text and return a list of list of
        english and chinese text of this article
        """
        URL = url + "dual/"

        self.crawler.get(URL)

        ch_text = [] # chinese sentence
        en_text = [] # english sentence
        tr_text = [] # sentence translated from chinese to english

        try:    
            elements = self.crawler.find_elements_by_css_selector(self.CSS_SELECTOR)

            for i in range(len(elements) - 1):
                en, ch = elements[i].text.split("\n")
                en_text.append(en)
                ch_text.append(ch)

                # translate chinese to english
                tmp_translated = self.translator.translate(ch)
                tr_text.append(tmp_translated)

        except:
            raise ValueError("Unable to extract content from URL:", URL)

        return (en_text, ch_text, tr_text)

if __name__ == "__main__":
    # driver
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pages', '-num', required=True, help='Number of pages to scrape on New York Times')
    args = parser.parse_args()

    link_scraper = LinkScraper(args)
    link_scraper.scrape()
