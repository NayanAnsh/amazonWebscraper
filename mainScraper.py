import requests
from bs4 import BeautifulSoup
RAW_URL = "https://www.amazon.in/AMD-Ryzen-3600-Processor-100000031BOX/dp/B07STGGQ18/ref=sr_1_4?dchild=1&keywords=3600&qid=1596975477&sr=8-4"






def makeConnection():
        #Amazon is denying service(error code 503) without user agent
    req =  requests.get(RAW_URL,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"})
    
    if not(req.status_code == 200):
        print("Something is wrong - \n error code - \n ",req.status_code)
        SystemExit()
    else:
        print("Successful Connection")
        return req


def getPrice(bs4soup):
        
    PRICE_RAW =  bs4soup.find(id = "priceblock_ourprice").get_text()
    price =  int(PRICE_RAW.replace("₹","").replace(",","").replace(".00","").strip())
    return price


req = makeConnection()
soup =  BeautifulSoup(req.content,"html.parser")
price = getPrice(soup)
print(price)  


