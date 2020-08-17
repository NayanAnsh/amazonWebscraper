import requests
import sqlite3 as sql
import os
from datetime import date
from bs4 import BeautifulSoup
import matplotlib.pyplot as pyplot
import sys
import re
from adjustText import adjust_text
#TODO: (Critical BUG)program is not storing data in databse when run by task scheduler(Need testing)
# Todone : (BUG)(FIXED)beautify the pyplot.annotion implement this library for better results
#        https://github.com/Phlya/adjustText
# Todo : add program to notify for specific price drop from previous day 
# Todo:  add mailing system to mail the price drop
# Todo: enable program to automatically write itself in task scheduler 
#       with users permition:



RAW_URL = ["https://www.amazon.in/AMD-Ryzen-3600-Processor-100000031BOX/dp/B07STGGQ18/ref=sr_1_4?dchild=1&keywords=3600&qid=1596975477&sr=8-4"
           ,"https://www.amazon.in/LG-inch-60-96-Gaming-Monitor/dp/B06XDY3SJF/ref=sr_1_5?crid=2O80YIB7ESTM9&dchild=1&keywords=monitor+ips+1ms&qid=1597508358&s=computers&sprefix=monitor+ips+1ms%2Ccomputers%2C436&sr=1-5"
           ,"https://www.amazon.in/ASUS-Prime-B450M-A-Motherboard-DDR4/dp/B07F6YQV4J/ref=sr_1_8?crid=KP16TPABINFP&dchild=1&keywords=motherboard+for+3rd+gen+ryzen&qid=1597508585&s=computers&sprefix=motherboard+for+3rd%2Ccomputers%2C309&sr=1-8"
           ,"https://www.amazon.in/HyperX-3200MHz-Desktop-Memory-HX432C16FB3/dp/B07WJJ9CNG/ref=sr_1_1?crid=2AFMX0JY5BNH5&dchild=1&keywords=ram+3200mhz&qid=1597508860&s=computers&sprefix=ram+3200%2Ccomputers%2C305&sr=1-1"]
FILEPATH = os.getcwd()
today = str(date.today())




def makeConnection(index):
        #Amazon is denying service(error code 503) without user agent Header
    req =  requests.get(RAW_URL[index],headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"})

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

def getProductName(bs4soup):
    PRODUCTNAME_RAW =  bs4soup.find(id = "productTitle").get_text()
    productName = PRODUCTNAME_RAW.strip()
    return productName





#################### DATABASE(AmazonDatabase.db) #####################
def executeSql(query):
    output = ""
    conn =  sql.connect(FILEPATH +"\database\\"+"AmazonDatabase"+".db")
    c =  conn.cursor()
    try:

        c.execute(query)

        output = c.fetchall()
        conn.commit()



    except sql.OperationalError as e:

        print(e)
    except sql.IntegrityError as e:
        print("Entry with this date has been already made, error message -\n",e)
    conn.close()
    return output



def createDB():
    executeSql("CREATE TABLE "+tableName+"(date PRIMARY KEY,price)")
def insertDB(values):
    executeSql("INSERT INTO "+table+" VALUES "+values)
def searchDB(columnName = "*",where = ""):
    if where  == "":
        return executeSql('SELECT ' +columnName+ ' FROM '+tableName)
    else :
        return executeSql('SELECT ' +columnName+ ' FROM '+tableName  + ' where '+where)
def deleteDB(condition):
    if condition != "":
        executeSql('DELETE FROM '+ tableName +' WHERE ' +condition)
    else:
        print("WARNING!! you just attempted to delete whole table!!")

def getTableName(name):
    #A code from stackoverflow modified regex little bit
    regex = re.compile('[^a-zA-Z1-9\s]')
    #First parameter is the replacement, second parameter is your input string
    return regex.sub('', name).replace(" ","_")

########################### GRAPH ###################
def getDateList():
    dateListRaw =  searchDB(columnName = "date")
    dateList = []
    for  d in dateListRaw:
        dateList.append(str(d[0]))
    return dateList

def getPriceList():
    priceListRaw = searchDB(columnName= "price")
    priceList =[]
    for p  in priceListRaw:
        priceList.append(int(p[0]))
    return priceList
def labelDataPoints(priceList):
    
    text = []
    for i in range(0,len(priceList)):
       text.append(pyplot.text(i, priceList[i], str(priceList[i])))
    adjust_text(text,arrowprops=dict(arrowstyle='->', color='red')) 
    
def showGraph():
    
    dateList = getDateList()
    priceList = getPriceList()
    pyplot.plot(dateList,priceList)
    pyplot.suptitle(productNameShort)
    pyplot.xlabel("Date")
    pyplot.ylabel("price")
    pyplot.yticks(range(round(int(min(priceList)/1.1),-3),int(max(priceList)*1.1),500))
    labelDataPoints(priceList) # must call this  method at last or just berfore pyplot.show() function
       
    
    pyplot.show()
    
################# MAIN #############
for i in range(0,len(RAW_URL)):
    #make connection and extract data
    req = makeConnection(i)
    soup =  BeautifulSoup(req.content,"html.parser")
    productPrice = getPrice(soup)
    productName =getProductName(soup)
    productNameShort =  productName[0:45]
    productNameShort =  productNameShort[0:productNameShort.rindex(" ")] #removes incomplete words

    #databse work
    tableName = getTableName(productNameShort)
    table = tableName+"(date,price)"
    values = '("'+ today +'" , "'+str(productPrice)+'")'
    createDB()
    insertDB(values)

    #graph work
    showGraph() #Disabled This method prevent fuction of task schedulaer decomment it if want to see graph
    
    
    #show database
    print("All commands executed showing database table")
    print(tableName)
    print(searchDB())
    print()

sys.exit(0)





