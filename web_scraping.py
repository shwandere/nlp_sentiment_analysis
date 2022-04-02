import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

header = {'User-Agent': 'Chrome/39.0.2171.95'}
os.environ['HTTP_PROXY']="http://127:0:0:1:8000"

loc = "F:\internship\\blackcoffer\Input.xlsx"


wb = pd.read_excel(loc,sheet_name='Sheet1',engine='openpyxl')
data = pd.DataFrame(wb, columns=['URL_ID','URL'])


for x in range(data.size):
    URL_ID = data.URL_ID[x]
    URL = data.URL[x]
    
    print(URL)

    page = requests.get(URL,headers=header)
    soup = BeautifulSoup(page.content,'html.parser')
    t=soup.find("h3")

    if (t!=None and t.attrs=={'class':['entry-title', 'td-module-title']}):
        s = t.findNext("h3")
        t.decompose()
        t = s
        
        #input()
        #t = s

    while(1):
        
        if (t!=None and t.attrs=={'class':['entry-title', 'td-module-title']}):
            
            s = t.findNext("h3")
            t.decompose()
            t = s

        elif (t==None):
            break
        elif (t.attrs!={'class':['entry-title', 'td-module-title']}):
            t = t.findNext("h3")
            continue
        else :
            continue
            

    results = soup.find("article")

    t = results.find(itemprop="headline ")
    title=t['content']
    print(title)
    print("\n")

    text = str()
    for para in results.find_all(["p","h3"]):
        temp = para.getText()
        temp = temp + "\n"
        text = text + temp
        
    print(text)
    folder_name = "F:\\internship\\blackcoffer\\text\\"
    file_name = folder_name + str(URL_ID) + ".txt"
    with open(file_name,'w', encoding="utf-8") as file:
        file.write(text)

