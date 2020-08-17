import sqlite3
import os
from datetime import date
import random
import matplotlib.pyplot as pyplot
from adjustText import adjust_text
path = os.getcwd()
databaseName =  "testDataBase.db"
conn = sqlite3.connect(path+"/"+databaseName)
c= conn.cursor()

today = str(date.today())
try:
    c.execute("CREATE TABLE sample(date PRIMARY KEY ,text1,text2)")
except sqlite3.OperationalError as e:
    print(e)
q = 'INSERT INTO sample(date,text1,text2) VALUES("'+str(random.randrange(1,100))+'","'+str(random.randrange(1,1000)) +'","sampletext2")'
try:
    
    c.execute(q)
except :
    print("unable to enter need unique data")
conn.commit()
#c.execute('DELETE FROM sample WHERE text1 = "sampletext1" ' )
c.execute('SELECT * FROM sample')
print(c.fetchall())

c.execute('SELECT date FROM sample')
dateList = c.fetchall()
c.execute('SELECT text1 FROM sample')
priceList = c.fetchall()

#pyplot.plot(dateList,priceList)
#pyplot.show()
conn.commit()
conn.close()
dates = []
for d in dateList:
    dates.append(d[0])

prices = []
for p in priceList:
    prices.append(int(str(p[0])))
pyplot.plot(dates,prices)
adjust_text([pyplot.text(i, prices[i], str(prices[i])) for i in range(0,len(prices))])
pyplot.show()