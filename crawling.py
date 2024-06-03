from text_preprocessing import get_preprocessed_text_terms
import re
import pandas as pd
import requests
from http.client import RemoteDisconnected
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import requests
from http.client import RemoteDisconnected
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def expand_document_with_crawled_data(doc_content: str) -> str:
    """
    This method takes a document content string as input and returns a string with crawled data from any URLs present in the input document content.

    The method first extracts URLs from the input document content using the __extractURLs function.
    If there are any URLs present, it crawls the text from each URL using the __crawl function and returns the crawled text.
    Finally, it returns the crawled data.

    Args:
        doc_content: The input document content string.
    Returns:
        The crawled data string.
    """
    document_included_urls = __extractURLs(doc_content)
    crawled_content = ''
    if len(document_included_urls) > 0:
        for url in document_included_urls:
            crawled_text = __crawl(url)
            crawled_content += crawled_text
    return crawled_content


def __extractURLs(content):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    return urls



def __is_text_url(url):

    response = requests.head(url)
    content_type = response.headers['Content-Type']
    content_disposition = response.headers.get('Content-Disposition', '')
    if 'text' in content_type and 'attachment' not in content_disposition:
        resource = urlparse(url).path
        file_extension = resource.split('.')[-1]
        text_file_extensions = ['txt', 'html', 'htm', 'xml', 'csv', 'json', 'md', 'rst', 'php', 'asp', 'aspx', 'css',
                                'js', 'py', 'rb', 'java', 'c', 'cpp', 'h', 'sh', 'bat', 'log', 'ini', 'conf', 'yml',
                                'yaml']
        if file_extension in text_file_extensions:
            return True
        response = requests.get(url, stream=True)
        content = response.raw.read(1024)
        if all(32 <= c < 127 or c in (9, 10, 13) for c in content):
            return True

    return False



def __crawl(url):
    try:
        if __is_text_url(url):
            print(f"crawling {url}")
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()  
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        else:
            return ''
    except (HTTPError, URLError, RemoteDisconnected) as e:
        return ''
    except Exception as e:
        return ''


__all__ = ['expand_document_with_crawled_data']
