from selenium import webdriver

class Crawler:
    def __init__(self):
        self.browser = webdriver.Chrome('/Users/baekchunkim/Downloads/chromedriver')

    def getBrowser(self):
        return self.browser


class LinkScraper(Crawler):
    def __init__(self):
        # initialize a cralwer object
        super(LinkScraper, self).__init__()
        self.crawler = self.browser

        # initial URL to NYC internaitonal articles homepage
        self.URL = "https://cn.nytimes.com/world/{PAGE_NUM}/"

        # scrape up to this page number
        self.MAX_PAGE_NUM = 2

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
            for url in links:        
                bi_text = scraper.extract(url)
        
                # write to file
                self.write(bi_text)

    def write(self, text):
        """
        Write bitext article to a txt file
        """

        # Set the filename
        template = "output__{NUM}.txt"
        filename = template.format(
            NUM=format(self.FILE_NUM, "03")
        )

        with open(filename, 'w') as output:
            for en in text[0]:
                output.write(en + "\n")
            
            # separate by asterisks
            output.write("************************************************************" + "\n")
            
            for ch in text[1]:
                output.write(ch + "\n")
            
        # increment the file number
        self.FILE_NUM += 1

class ArticleScraper(Crawler):

    def __init__(self):
        super(ArticleScraper, self).__init__()
        self.crawler = self.browser
        self.SELECTOR = "div.bilingual.cf > div.cf.articleContent"

    def extract(self, url):
        """
        For each article, separate the chinese and english text and return a list of list of
        english and chinese text of this article
        """
        URL = url + "dual/"

        self.crawler.get(URL)

        ch_text = []
        en_text = []

        try:    
            elements = self.crawler.find_elements_by_css_selector(self.SELECTOR)

            for i in range(len(elements) - 1):
                en, ch = elements[i].text.split("\n")
                en_text.append(en)
                ch_text.append(ch)

        except:
            print("ERROR!! on URL:", URL)

        return (en_text, ch_text)

if __name__ == "__main__":
    # driver
    link_scraper = LinkScraper()
    link_scraper.scrape()
