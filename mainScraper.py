import requests

RAW_URL = "https://www.amazon.in/AMD-Ryzen-3600-Processor-100000031BOX/dp/B07STGGQ18/ref=sr_1_4?dchild=1&keywords=3600&qid=1596975477&sr=8-4"

req =  requests.get(RAW_URL)
print(req.text)