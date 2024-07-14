
# Web Crawler README
![Webtype](./web_type.jpg)
## Overview
This project provides classes for scraping data from web pages. There are two main classes:
1. SinglePage_WebCrawler
2. MultiPage_WebCrawler

Each class provides various methods to extract data from web pages, and there is also a utility function to insert data into a MongoDB database.

## Installation
Before using these classes, ensure you have the required dependencies installed:
```bash
pip install selenium beautifulsoup4 requests tqdm pymongo
```

## Note
Additionally, install the supported ChromeDriver for your version of the Chrome browser.

## Classes and Methods
### 1. SinglePage_WebCrawler
This class is used for scraping data from a single web page that does not include multiple pages inside.

Initialization
```python
crawler = SinglePage_WebCrawler(url, html_check=True, category='Not defined', owner_source='Not defined')
```
- url (str): The URL to scrape data from.
- html_check (bool, optional): Flag to indicate whether the content is HTML or not. Defaults to True.
- category (str, optional): The category of the web page. Defaults to 'Not defined'.
- owner_source (str, optional): The source of the web page. Defaults to 'Not defined'.


#### Methods
- get_text()
Retrieves and joins the text content from the webpage.

```python
text = crawler.get_text()
```

- get_title()
Returns the text content of the title tag from the webpage.

```python
title = crawler.get_title()
```

- get_images(image_area_tag=None, image_area_class=None)
Retrieves the URLs of all images from a specific area of the webpage.

```python
images = crawler.get_images(image_area_tag='div', image_area_class='image-class')
```
- get_banner_image(banner_tag='src', banner_class=None)
Retrieves the URL of the banner image from the webpage.

```python
banner = crawler.get_banner_image(banner_class='banner-class')
```
- get_content(title_tag=None, title_class=None, content_area_tag=None, content_area_class=None)
Retrieves the title and content from the webpage based on the specified tags and classes.

```python
title, content = crawler.get_content(title_tag='h1', title_class='title-class', content_area_tag='div', content_area_class='content-class')
```
### 2. MultiPage_WebCrawler
This class inherits from SinglePage_WebCrawler and is used for scraping data from multiple pages within a website.

Initialization
```python
crawler = MultiPage_WebCrawler(url, html_check=True, category='Not defined', owner_source='Not defined')
```
Same parameters as SinglePage_WebCrawler.

#### Methods
- get_pages_url_list(start_page=1, end_page=1, step_page=1, a_class=None, custom_pageindex_list=None)
Retrieves a list of URLs for web pages based on specified criteria.

```python
pages = crawler.get_pages_url_list(start_page=1, end_page=5, a_class='page-link-class')
```

- get_articles(tag_dict)
Retrieves articles from a list of URLs based on the provided tag dictionary.

```python
tag_dict = {
    'url': 'https://example.com/page={0}',
    'start_page': 1,
    'end_page': 5,
    'step_page': 1,
    'a_class_in_PageList': 'article-link-class',
    'title_tag_in_ArticlePage': 'h1',
    'title_class_in_ArticlePage': 'title-class',
    'content_area_tag_in_ArticlePage': 'div',
    'content_area_class_in_ArticlePage': 'content-class',
    'banner_tag_in_ArticlePage': 'src',
    'banner_class_in_ArticlePage': 'banner-class',
    'custom_pageindex_list': None
}
articles = crawler.get_articles(tag_dict)
```

#### Utility Function
insert_contents_to_mongoDB(database_address, database_name, database_colection, contents_list)
Inserts contents into a MongoDB database.

```python
insert_contents_to_mongoDB(
    database_address='mongodb://localhost:27017/',
    database_name='myDatabase',
    database_colection='myCollection',
    contents_list=articles
)
```

## Example Usage
#### Single Page Crawler
```python
crawler = SinglePage_WebCrawler('https://example.com', html_check=True)
text = crawler.get_text()
title = crawler.get_title()
images = crawler.get_images('div', 'image-class')
banner = crawler.get_banner_image('src', 'banner-class')
title, content = crawler.get_content('h1', 'title-class', 'div', 'content-class')
```

#### MultiPage Crawler
```python
from WebScraping_Crawler import MultiPage_WebCrawler
url = 'https://www.bangkokhospital.com/health-info/disease-treatment?page={0}'
web_crawler = MultiPage_WebCrawler(url, html_check=False, category="healthcare", owner_source="Bangkok Hospital")
web_tag = {
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
content = web_crawler.get_articles(web_tag)
```
#### Insert Articles into MongoDB
```python

insert_contents_to_mongoDB(
    database_address='mongodb://localhost:27017/',
    database_name='myDatabase',
    database_colection='myCollection',
    contents_list=articles
)
```
