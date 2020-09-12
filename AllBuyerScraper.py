# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 09:54:58 2020

@author: Nayan
"""


import requests

def getPriceFromSellersList(RAW_URL):


    OTHER_BUYERS_CONSTANT = "/ref=dp_olp_unknown_mbc"
    CurrentUrl = RAW_URL
    start = CurrentUrl.index("/B0")+1
    end = CurrentUrl.index("/",CurrentUrl.index("/B0") +1)
    PRODUCT_UNIQUE_CODE = CurrentUrl[start:end]
    ALL_BUYER_URL = "https://www.amazon.in/gp/offer-listing/"+PRODUCT_UNIQUE_CODE+OTHER_BUYERS_CONSTANT

    req =  requests.get(ALL_BUYER_URL,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"})
    st = str(req.content)
    srt ='<span class="currencyINRFallback" style="display:none">Rs. </span>'
    first=st.index(srt)
    return st[first+len(srt):st.index("</span>",first+len(srt))]

s=getPriceFromSellersList("https://www.amazon.in/LG-inch-60-96-Gaming-Monitor/dp/B06XDY3SJF/ref=sr_1_5?crid=2O80YIB7ESTM9&dchild=1&keywords=monitor+ips+1ms&qid=1597508358&s=computers&sprefix=monitor+ips+1ms%2Ccomputers%2C436&sr=1-5")
print(s)