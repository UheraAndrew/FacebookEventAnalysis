import urllib.request
from bs4 import BeautifulSoup
def main():
    all_urls = []
    url1 = ""
    url2 = " "
    for i in range(1, 10000):

        url = "https://2event.com/uk/events/page-" + str(i) + "?city=lviv"
        text = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(text, )

        temp = ["https://2event.com" + a['href'] for a in
                soup.find_all(attrs={"class": "event-link"})]
        url1 = temp[0]
        if url1 == url2:
            break

        url2 = url1
        all_urls.extend(temp)
    corected = []
    for url in all_urls:
        url=url.split('/')[-1]
        corected.append(url)
    return corected