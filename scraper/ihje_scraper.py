from selenium import webdriver
from time import sleep
from random import randrange
import pandas as pd


class IHJEScraper:
    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.driver = webdriver.Chrome(executable_path)

    def get_abstracts(self,volume_number,issue_number):
        titles = []
        authors = []
        abstracts = []
        page_ranges = []
        urls = []
        url = f"https://www.sciencedirect.com/journal/international-journal-of-hydrogen-energy/vol/{volume_number}/issue/{issue_number}"
        self.driver.get(url)
        sleep(randrange(10,15))
        articles = self.driver.find_elements('class name','js-article')
        # click button to reveal abstract
        for article in articles:
            buttons = article.find_elements('class name','tab-title')
            for button in buttons:
                sleep(randrange(2,4))
                if button.text == 'Abstract':
                    try:
                        button.click()
                        break
                    except:
                        print('button was not needed. continuing')
                        break
                    
            try:
                title = article.find_element('class name','js-article-title').text
                author_list = article.find_element('class name','js-article-author-list').text
                abstract = article.find_element('class name','js-abstract-body-text').text
                page_range = article.find_element('class name','js-article-page-range').text
                urls.append(url)
                titles.append(title)
                authors.append(author_list)
                page_ranges.append(page_range)
                abstracts.append(abstract)

            except Exception as e:
                print('Error while scraping this article: ', e)
                continue

        self.abstracts_df = pd.DataFrame({'title':titles, 'authors':authors, 'abstract':abstracts, 'page_range':page_ranges, 'url':urls})
        return self.abstracts_df

    def get_journal_structure(self,url):
        """Return a dictionary where the key is the section of the issue, and value is a list of all 
        articles in that section"""

        self.journal_structure = {}
        self.driver.get(url)
        sleep(randrange(10,15))
        section_titles = self.driver.find_elements('class name','js-section-title-level-1')
        for section in section_titles:
            section_parent = section.find_element('xpath','..')
            articles_in_section = section_parent.find_elements('class name','js-article-title')  
            articles = [] 
            for article in articles_in_section:
                articles.append(article.text)

            self.journal_structure[section.text] = articles
        return self.journal_structure
    