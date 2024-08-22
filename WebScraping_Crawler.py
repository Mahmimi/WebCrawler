"""CITE: https://github.com/Mahmimi/WebCrawler"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from tqdm.auto import tqdm
import warnings
from pymongo import MongoClient

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
warnings.filterwarnings("ignore", category=UserWarning)

"""
    TODO: please install supported ChromeDriver with your chrome browser before use.
"""

class SinglePage_WebCrawler():

    """
    Single Page Web Crawler use for scraping data from single web page which not include multiple pages inside. For example
    URL = 'https://www.bangkokinternationalhospital.com/th/health-articles/disease-treatment/trigger-finger-treatment' 
    can be used.

    """

    def __init__(self, url:str, html_check:bool=True, category:str='Not defined', owner_source:str='Not defined', as_connector:bool=False, driver:webdriver.Chrome=None, show_progressbar:bool=True):
        """
        Initialize the SinglePage_WebCrawler with the specified URL and HTML check flag.
        
        Parameters:
            url (str): The URL to scrape data from.
            html_check (bool, optional): Flag to indicate whether the content is HTML or not. Defaults to True. Please see Note below if error or content is not found.
            category (str, optional): The category of the web page. Defaults to None.
            owner_source (str, optional): The source of the web page. Defaults to None.
            as_connector (bool, optional): if True, the driver will not refresh the page or reload the page. Defaults to False.
            driver (webdriver.Chrome, optional): The webdriver to use. Defaults to None.
            show_progressbar (bool, optional): If True, show a progress bar. Defaults to True.
        
        Returns:
            None
        
        Note:
            html_check also check static content if html_check is True and dynamic content if html_check is False. 
            If you are unsure about this flag, try scraping with html_check=True first. If content is not found, try html_check=False.
        
        Suggession:
            If you want to scrape more content than provided built-in functions, use SinglePage_WebCrawler.soup with single driver will be efficient.
            For example:

            >>>    from WebScraping_Crawler import SinglePage_WebCrawler,MultiPage_WebCrawler,insert_contents_to_mongoDB
            >>>    from tqdm.auto import tqdm
            >>>    import pandas as pd
            >>>    from selenium import webdriver
            
            >>>    url = 'https://www.kaidee.com/c221-pet-cat/p-{0}'
            >>>    web_crawler = MultiPage_WebCrawler(url, html_check=False, category="pet", owner_source="Kaidee")
            >>>    url_list = web_crawler.get_pages_url_list(a_class='sc-1n24v7v-0 kERWEr box-border overflow-hidden', start_page=1, end_page=5, step_page=1)

            >>>    # Initialize a WebDriver instance
            >>>    options = webdriver.ChromeOptions()
            >>>    options.add_argument('--headless')
            >>>    options.add_argument('--disable-gpu')
            >>>    options.add_argument("--no-sandbox")
            >>>    options.add_argument("--disable-dev-shm-usage")
            >>>    options.add_argument("--window-size=1920,1080")
            >>>    options.add_argument("start-maximized")
            >>>    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            >>>    driver = webdriver.Chrome(options=options)
            >>>    driver.implicitly_wait(10)

            >>>    # Initialize an empty list to collect data
            >>>    data = []

            >>>    for page in tqdm(url_list, desc='Page number'):
            >>>        try:
            >>>            web_crawler = SinglePage_WebCrawler(page, html_check=False, category="pet", owner_source="Kaidee", driver=driver)
            >>>            title = web_crawler.get_title()
            >>>            price = float(web_crawler.soup.find('span', class_="sc-3tpgds-0 iBWLya sc-1q2fzk2-2 ehoPiE").text.replace(' ', '').replace('฿', '').replace(',',''))
            >>>            seller = web_crawler.soup.find('a', class_="sc-1f9a7ae-0 grxgwt font-bold text-sd125").text
            >>>            tag = web_crawler.soup.find('div', class_="my-lg mx-0 relative flex flex-wrap items-center gap-sm overflow-hidden").text
            >>>            species = web_crawler.soup.find('div', class_="grid grid-cols-1 md:grid-cols-2 md:gap-x-5xl").text
            >>>            description = web_crawler.soup.find('div', class_="sc-1ir8548-0 kPXKAP").text.replace('อ่านเพิ่มเติม', '')
            >>>            province = tag.split('/')[-2]
            >>>            district = tag.split('/')[-1]
            >>>            # Append data to list
            >>>            data.append({
            >>>                'Title': title,
            >>>                'Price': price,
            >>>                'Seller': seller,
            >>>                'Tag': tag,
            >>>                'Species': species,
            >>>                'Description': description,
            >>>                'Province': province,
            >>>                'District': district
            >>>            })
            >>>        except:
            >>>            continue

            >>>    # Create DataFrame from collected data
            >>>    df = pd.DataFrame(data)
        """

        self.url = url
        self.html_check = html_check
        self.category = category
        self.owner_source = owner_source
        self.driver = driver
        self.as_connector = as_connector
        self.show_progressbar = show_progressbar

        if html_check:
            source = requests.get(self.url)
            self.soup = BeautifulSoup(source.content,'html.parser', from_encoding='utf-8')
        
        else:

            if not self.driver:
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("start-maximized")
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                self.driver = webdriver.Chrome(options=options)
                self.driver.implicitly_wait(10)
            else:
                self.driver = driver

            if not as_connector:
                self.driver.get(self.url)

            html = self.driver.page_source
            self.soup = BeautifulSoup(html, from_encoding='utf-8')

    def get_text(self):
        """
        This function retrieves and joins the text content from the webpage soup object.
        No parameters are passed to this function.
        Returns the joined text content as a string.
        """

        text = ' '.join(self.soup.text.split())
        return text
    
    def get_title(self):
        """
        Returns the text content of the title tag from the BeautifulSoup object.

        :return: A string representing the text content of the title tag.
        """

        return self.soup.title.text

    def get_images(self, image_area_tag:str=None, image_area_class:str=None):
        """
        Retrieves the URLs of all images from a specific area of the webpage.

        Args:
            image_area_tag (str, optional): The HTML tag of the image area. Defaults to None.
            image_area_class (str, optional): The CSS class of the image area. Defaults to None.

        Returns:
            list: A list of URLs of all images in the specified area.
        """

        soup = self.soup.find(image_area_tag, class_=image_area_class)
        images = list()
        for img in soup.find_all('img'):
            if img['src'].lower().endswith(('.jpg', '.jpeg', '.png')):
                images.append(img['src'])
        return images

    def get_banner_image(self, banner_tag:str='src' , banner_class:str=None):
        """
        Retrieves the URL of the banner image from the webpage.

        Args:
            banner_tag (str, optional): The HTML attribute of the banner image tag. Defaults to 'src'.
            banner_class (str, optional): The CSS class of the banner image tag. Defaults to None.

        Returns:
            str: The URL of the banner image.
        """

        banner = self.soup.find('img', class_=banner_class)[banner_tag]
        return banner

    def get_content(self, title_tag:str=None, title_class:str=None, content_area_tag:str=None, content_area_class:str=None):
        """
        Retrieves the title and content from the webpage based on the specified tags and classes.

        Args:
            title_tag (str, optional): The HTML tag for the title. Defaults to None.
            title_class (str, optional): The CSS class of the title. Defaults to None.
            content_area_tag (str, optional): The HTML tag for the content area. Defaults to None.
            content_area_class (str, optional): The CSS class of the content area. Defaults to None.

        Returns:
            tuple: A tuple containing the title and content extracted from the webpage.
        """

        try:
            title = ' '.join(self.soup.find(title_tag, class_=title_class).stripped_strings)
            content = self.soup.find(content_area_tag, class_=content_area_class).text.split()
        except:
            title = ''
            content = self.soup.find().text.split()
            
        return title, content

class MultiPage_WebCrawler(SinglePage_WebCrawler):

    """
    Multi Page Web Crawler use for scraping data from single web page which include multiple pages inside. For example
    URL = 'https://www.bangkokhospital.com/health-info/disease-treatment?page={0}' 
    can be used.

    Note:
        If any url of multipage changed when selecting next page, like 'page={0}' to 'page={1}'. You can only pass the string of url
        like 'page={0}' or any integer.
    """

    def _local_html_webscraping(self,url:str=None):
        """
        Perform webscraping on a local URL. If no URL is provided, it uses the default URL.
        
        Parameters:
            url (str, optional): The URL to scrape data from. Defaults to None.
        
        Returns:
            BeautifulSoup: Parsed HTML content of the webpage.
        """

        soup = None
        local_url = None
        if url:
            local_url = url
        else:
            local_url = self.url
        
        if self.html_check:
            source = requests.get(local_url)
            soup = BeautifulSoup(source.content,'html.parser', from_encoding='utf-8')
        else:
            print('Invalid html_check, html_check must be html_check=True.')

        return soup

    def _local_not_html_webscraping(self,url:str=None):
        """
        Perform webscraping on a local URL. If no URL is provided, it uses the default URL.
        
        Parameters:
            url (str, optional): The URL to scrape data from. Defaults to None.
        
        Returns:
            BeautifulSoup: Parsed HTML content of the webpage.
        """

        soup = None
        local_url = None

        if url:
            local_url = url
        else:
            local_url = self.url

        if not self.html_check:
            if not self.as_connector:
                self.driver.get(local_url)
            html = self.driver.page_source
            soup = BeautifulSoup(html, from_encoding='utf-8')
        else:
            print('Invalid html_check, html_check must be html_check=False.')

        return soup
    
    def _local_web_scraping(self,url:str=None):
        """
        Perform webscraping on a local URL. If no URL is provided, it uses the default URL.
        
        Parameters:
            url (str, optional): The URL to scrape data from. Defaults to None.
        
        Returns:
            BeautifulSoup: Parsed HTML content of the webpage.
        """

        if self.html_check:
            soup = self._local_html_webscraping(url)
        else:
            soup = self._local_not_html_webscraping(url)

        return soup

    def _local_get_content_sep(self,soup:BeautifulSoup=None, title_tag:str=None, 
                               title_class:str=None, content_area_tag:str=None, content_area_class:str=None):
        """
        Retrieves the title and content from the given BeautifulSoup object.

        Args:
            soup (BeautifulSoup, optional): The BeautifulSoup object to scrape data from. Defaults to None.
            title_tag (str, optional): The HTML tag for the title. Defaults to None.
            title_class (str, optional): The CSS class of the title. Defaults to None.
            content_area_tag (str, optional): The HTML tag for the content area. Defaults to None.
            content_area_class (str, optional): The CSS class of the content area. Defaults to None.

        Returns:
            tuple: A tuple containing the title and content extracted from the BeautifulSoup object.

        Raises:
            None
        """
        
        try:
            title = ' '.join(soup.find(title_tag, class_=title_class).stripped_strings)
            content = soup.find(content_area_tag, class_=content_area_class).text.split()
            
        except:
            title = soup.title.text
            content = soup.find().text.split()

        return title, content

    def _local_get_banner_image_sep(self,soup:BeautifulSoup=None, banner_tag:str='src',banner_class:str=None):
        """
        Retrieves the banner image from a BeautifulSoup object.

        Args:
            soup (BeautifulSoup, optional): The BeautifulSoup object to search for the banner image. Defaults to None.
            banner_tag (str, optional): The HTML attribute of the banner image tag. Defaults to 'src'.
            banner_class (str, optional): The CSS class of the banner image tag. Defaults to None.

        Returns:
            str: The URL of the banner image.

        Raises:
            None
        """

        banner = soup.find('img', class_=banner_class)[banner_tag]
        
        return banner
    
    def _local_get_images_sep(self,soup:BeautifulSoup=None, image_area_tag:str=None, image_area_class:str=None):
        """
        Retrieves a list of image URLs from a BeautifulSoup object.

        Args:
            soup (BeautifulSoup, optional): The BeautifulSoup object to search for images. Defaults to None.
            image_area_tag (str, optional): The HTML tag of the image area. Defaults to None.
            image_area_class (str, optional): The CSS class of the image area. Defaults to None.

        Returns:
            list: A list of image URLs.
        """

        soup = soup.find(image_area_tag, class_=image_area_class)
        images = list()
        for img in soup.find_all('img'):
            if img['src'].lower().endswith(('.jpg', '.jpeg', '.png')):
                images.append(img['src'])
            
        return images

    def get_pages_url_list(self, start_page:int=1, end_page:int=1, step_page:int=1, 
                           a_class:str=None, custom_pageindex_list:list=None):
        """
        Retrieves a list of URLs for web pages based on specified criteria.

        Args:
            start_page (int, optional): The starting page number. Defaults to 1.
            end_page (int, optional): The ending page number. Defaults to 1.
            step_page (int, optional): The step for page iteration. Defaults to 1.
            a_class (str, optional): The CSS class of the page element. Defaults to None.
            custom_pageindex_list (list, optional): A list of custom page indexes. Defaults to None.

        Returns:
            list: A list of unique URLs for the web pages.
        """
        
        pages_list = []
        if self.show_progressbar:
            if custom_pageindex_list:
                for i in tqdm(custom_pageindex_list,desc='Page number'):
                    url = self.url.format(i)
                    soup = self._local_web_scraping(url=url)
            
                    for read_more in soup.find_all('a', class_=a_class, href=True):
                        if not read_more['href'].startswith('http'):
                            read_more['href'] = urljoin(url, read_more['href'])
                        pages_list.append(read_more['href'])

            else:
                for i in tqdm(range(start_page, end_page+1, step_page),desc='Page number'):
                    url = self.url.format(i)
                    soup = self._local_web_scraping(url=url)
            
                    for read_more in soup.find_all('a', class_=a_class, href=True):
                        if not read_more['href'].startswith('http'):
                            read_more['href'] = urljoin(url, read_more['href'])
                        pages_list.append(read_more['href'])
        else:
            if custom_pageindex_list:
                for i in custom_pageindex_list:
                    url = self.url.format(i)
                    soup = self._local_web_scraping(url=url)
            
                    for read_more in soup.find_all('a', class_=a_class, href=True):
                        if not read_more['href'].startswith('http'):
                            read_more['href'] = urljoin(url, read_more['href'])
                        pages_list.append(read_more['href'])

            else:
                for i in range(start_page, end_page+1, step_page):
                    url = self.url.format(i)
                    soup = self._local_web_scraping(url=url)
            
                    for read_more in soup.find_all('a', class_=a_class, href=True):
                        if not read_more['href'].startswith('http'):
                            read_more['href'] = urljoin(url, read_more['href'])
                        pages_list.append(read_more['href'])

        return list(set(pages_list))

    def get_articles(self, tag_dict:dict=None):
        """
        Retrieves articles from a list of URLs based on the provided tag dictionary.
        
        Args:
            tag_dict (dict, optional): A dictionary containing the tags and classes for scraping the articles. Defaults to None.
                - url (str): The URL of the main web page to scrape.
                - start_page (int): The starting page number for scraping.
                - end_page (int): The ending page number for scraping.
                - step_page (int): The step size for incrementing the page number.
                - article_area_class_in_PageList (str): The CSS class of the article area in the page list.
                - a_class_in_PageList (str): The CSS class of the anchor tag in the page list.
                - title_tag_in_ArticlePage (str): The HTML tag of the title in the article page.
                - title_class_in_ArticlePage (str): The CSS class of the title in the article page.
                - content_area_tag_in_ArticlePage (str): The HTML tag of the content area in the article page.
                - content_area_class_in_ArticlePage (str): The CSS class of the content area in the article page.
                - banner_tag_in_ArticlePage (str): The HTML tag of the banner image in the article page.
                - banner_class_in_ArticlePage (str): The CSS class of the banner image in the article page.
                - custom_pageindex_list (list, optional): A custom list of page indices to scrape. For example, [2, 4, 6, 8, 10]. Defaults to None.
        
        Returns:
            list: A list of dictionaries containing the scraped article information.
                - url (str): The URL of the article.
                - category (str): The category of the article.
                - title (str): The title of the article.
                - owner source (str): The owner source of the article.
                - content (str): The content of the article.
                - banner (str): The URL of the banner image.
                - image (list): A list of URLs of the images in the article.
        
        Raises:
            None
        
        Notes:
            - If the tag dictionary is not provided, an error message will be printed and an empty list will be returned.
            - If the tag dictionary is missing any required keys, an error message will be printed and an empty list will be returned.
            - If the scraping process encounters any errors, the URLs of the articles that failed to scrape will be stored in the `diff` list.
            - If the banner image is found in the list of images, it will be removed from the list.

        Example:
            >>> from WebScraping_Crawler import MultiPage_WebCrawler
            >>> url = 'https://www.bangkokhospital.com/health-info/disease-treatment?page={0}'
            >>> web_crawler = MultiPage_WebCrawler(url, html_check=False, category="healthcare", owner_source="Bangkok Hospital")
            >>> web_tag = {
                            'url' : url,
                            'start_page' : 1,
                            'end_page' : 1,
                            'step_page' : 1,
                            'article_area_class_in_PageList': "_w-100pct _h-100pct _dp-f _fdrt-cl _jtfct-spbtw _pd-12px _pd-16px-md",
                            'a_class_in_PageList' : '_dp-f _fdrt-cl _mgbt-32px _alit-str _h-100pct', 
                            'title_tag_in_ArticlePage' : 'h1',
                            'title_class_in_ArticlePage' : '_dp-ilb has-text-blue-primary _ttf-cptl _fs-3-md _w-100pct _w-at-sm -animated-underline -show-line _tal-ct fs-4',
                            'content_area_tag_in_ArticlePage':'div',
                            'content_area_class_in_ArticlePage':'container',
                            'banner_tag_in_ArticlePage':'src',
                            'banner_class_in_ArticlePage':'hero-img _w-100pct -transition-all -cover',
                            'custom_pageindex_list':None
                        }
            >>> content = web_crawler.get_articles(web_tag)


        """
        if not tag_dict:
            raise Exception("Tag dictionary is not provided. Please see the example.")

        title_return = None
        content_return = None
        banner_return = None
        image_return = None
        contents = []
        diff = []

        try:
            articles_url = self.get_pages_url_list(start_page=tag_dict['start_page'], end_page=tag_dict['end_page'], step_page=tag_dict['step_page'], 
                                                a_class=tag_dict['a_class_in_PageList'],custom_pageindex_list=tag_dict['custom_pageindex_list'])
        except:
            print(f"get_pages_url_list() can't get articles url. Please check web tag for {self.url}: (start_page|end_page|step_page|a_class_in_PageList|custom_pageindex_list)")

        if self.show_progressbar:
            for articles in tqdm(articles_url,desc='Article number'):
                try:
                    soup_sep = self._local_web_scraping(url=articles)
                    title_return, content_return = self._local_get_content_sep(soup=soup_sep, title_tag=tag_dict['title_tag_in_ArticlePage'], 
                                                                        title_class=tag_dict['title_class_in_ArticlePage'],
                                                                        content_area_tag=tag_dict['content_area_tag_in_ArticlePage'], 
                                                                        content_area_class=tag_dict['content_area_class_in_ArticlePage'])
                    if title_return == '':
                        #print("Can't find title. Please check web tag from :",articles)
                        continue
                    
                    if content_return == '':
                        #print("Can't find contents. Please check web tag from :",articles)
                        continue
                            
                    banner_return = self._local_get_banner_image_sep(soup=soup_sep, banner_tag=tag_dict['banner_tag_in_ArticlePage'], 
                                                                    banner_class=tag_dict['banner_class_in_ArticlePage'])
                    
                    if banner_return == None:
                        #print("Can't find banner. Please check web tag from :",articles)
                        pass

                    image_return = self._local_get_images_sep(soup=soup_sep, image_area_tag=tag_dict['content_area_tag_in_ArticlePage'], 
                                                                    image_area_class=tag_dict['content_area_class_in_ArticlePage'])
                    if image_return == []:
                        #print("Can't find images. Please check web tag from :",articles)
                        pass
                            
                    if banner_return in image_return:
                        image_return.remove(banner_return)
                    
                    contents.append({'url':articles,'category':self.category, 'title':title_return,'owner source':self.owner_source,
                                    'content':' '.join(content_return), 'banner':banner_return, 'image':image_return})
                    
            
                except:
                    diff.append(articles)
        else:
            for articles in articles_url:
                try:
                    soup_sep = self._local_web_scraping(url=articles)
                    title_return, content_return = self._local_get_content_sep(soup=soup_sep, title_tag=tag_dict['title_tag_in_ArticlePage'], 
                                                                        title_class=tag_dict['title_class_in_ArticlePage'],
                                                                        content_area_tag=tag_dict['content_area_tag_in_ArticlePage'], 
                                                                        content_area_class=tag_dict['content_area_class_in_ArticlePage'])
                    if title_return == '':
                        #print("Can't find title. Please check web tag from :",articles)
                        continue
                    
                    if content_return == '':
                        #print("Can't find contents. Please check web tag from :",articles)
                        continue
                            
                    banner_return = self._local_get_banner_image_sep(soup=soup_sep, banner_tag=tag_dict['banner_tag_in_ArticlePage'], 
                                                                    banner_class=tag_dict['banner_class_in_ArticlePage'])
                    
                    if banner_return == None:
                        #print("Can't find banner. Please check web tag from :",articles)
                        pass

                    image_return = self._local_get_images_sep(soup=soup_sep, image_area_tag=tag_dict['content_area_tag_in_ArticlePage'], 
                                                                    image_area_class=tag_dict['content_area_class_in_ArticlePage'])
                    if image_return == []:
                        #print("Can't find images. Please check web tag from :",articles)
                        pass
                            
                    if banner_return in image_return:
                        image_return.remove(banner_return)
                    
                    contents.append({'url':articles,'category':self.category, 'title':title_return,'owner source':self.owner_source,
                                    'content':' '.join(content_return), 'banner':banner_return, 'image':image_return})
                    
            
                except:
                    diff.append(articles)

        try:
            print('different url web type from the other are :',diff)
        except:
            pass

        return contents

#connect to mongodb
def insert_contents_to_mongoDB(database_address:str,database_name:str,database_colection:str,contents_list:list,show_progressbar:bool=True):

    """
	Inserts contents into a MongoDB database.

	Parameters:
	- database_address: str, the address of the MongoDB database.
	- database_name: str, the name of the database.
	- database_colection: str, the name of the collection in the database.
	- contents_list: list, a list of contents to be inserted.
    - show_progressbar: bool, whether to show the progress bar.

	Returns:
	- None
	"""

    try:
        client = MongoClient(database_address)

        print("---Connenction Successful---")

        database_name = client[database_name]

        database = database_name[database_colection]

        if show_progressbar:
            for i in tqdm(contents_list,desc='content number'):
                database.insert_one(i)
        else:
            for i in contents_list:
                database.insert_one(i)
        
        print('---Insert Successful---')

    except:
        print("Connection Fail")