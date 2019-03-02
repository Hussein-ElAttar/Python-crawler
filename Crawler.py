from bs4 import BeautifulSoup
from abc import abstractmethod,ABC
import urllib.request
import re

gretty_url    = "https://www.gettyimages.com/photos/{{keyword}}?alloweduse=availableforalluses&family=creative&license=rf&phrase={{keyword}}&sort=best#license"
bing_url      = "https://www.bing.com/search?q={{keyword}}+wikipedia+site%3Awikipedia.org&go=Search&qs=ds&form=QBRE"
yahoo_url     = "https://images.search.yahoo.com/search/images;_ylt=F;_ylc=X?&fr2=sb-top-images.search.yahoo.com&p={{keyword}}"
gretty_hq_url = "https://media.gettyimages.com/photos/picture-id"


class Image_Crawler(ABC):


    def __init__(self):
        self.urls = []
        self.keyword = ""


    def crawl_page(self, url):
        hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        req      = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        html     = response.read()
        return BeautifulSoup(html, 'html.parser')


    @abstractmethod
    def search(self, keyword):
        pass
    

    def get_urls(self):
        return self.urls


    def get_image_description(self):
        url       = bing_url.replace("{{keyword}}", self.keyword)
        crawler   = self.crawl_page(url)
        try:
            desc  = crawler.find("ul", { "class" : "b_vList" }).find("li").find("div")
            return desc.string
        except:
            return "Lorem Ipsum is simply dummy text"

class Gretty_Image_Crawler(Image_Crawler):


    def __init__(self,keyword):
        super().__init__()
        self.search(keyword)


    def search(self, keyword):
        self.urls = []
        self.keyword = keyword.replace(" ", "%20")
        url      = gretty_url.replace("{{keyword}}", self.keyword)
        crawler  = self.crawl_page(url)
        img_tags = crawler.findAll("a", {"class","search-result-asset-link"})
        for tag in img_tags:
            id = tag["data-asset-id"]
            self.urls.append(gretty_hq_url + id)

        return self.urls



class Yahoo_Image_Crawler(Image_Crawler):


    def __init__(self, keyword):
        super().__init__()
        self.search(keyword)

    
    def search(self, keyword):
        self.urls = []
        self.keyword = keyword.replace(" ", "%20")
        url      = yahoo_url.replace("{{keyword}}", self.keyword)
        crawler  = self.crawl_page(url)
        lis  = crawler.findAll("li",{"class":"ld"})
        for li in lis:
            a = li.find("a")
            href = a["href"]
            img_url = re.search(r'imgurl=(.*?)&rurl', href).group(1)
            img_url = img_url.replace("%2F", "/")
            self.urls.append(img_url)
