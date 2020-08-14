import requests
from bs4 import BeautifulSoup
RAW_URL = "https://www.amazon.in/AMD-Ryzen-3600-Processor-100000031BOX/dp/B07STGGQ18/ref=sr_1_4?dchild=1&keywords=3600&qid=1596975477&sr=8-4"

#Amazon is denying service(error code 503) without user agent
req =  requests.get(RAW_URL,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"})

if not(req.status_code == 200):
    print("Something is wrong - \n error code - \n ",req.status_code)
    SystemExit()

soup =  BeautifulSoup(req.content,"html.parser")

