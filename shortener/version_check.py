import requests
from bs4 import BeautifulSoup

def version_check():
    url = 'https://fg-anime.in/version'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        element = soup.find('p')
        
        version = element.get_text(strip=True)
        return version
