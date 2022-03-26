import requests
from bs4 import BeautifulSoup


def GI(keyword):
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(keyword + " star wars")
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')
    return images[1].get('src')

if __name__ == '__main__':
    x = GI("luke skywalker")
    print(x)