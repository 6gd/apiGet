from time import sleep
from typing import Optional


import threading


from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
from bs4 import BeautifulSoup
app = FastAPI()

origins = [
    "http://apiget-gv5f.onrender.com",
    "https://apiget-gv5f.onrender.com",
    "http://render.com",
    "https://render.com",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



LastList = []

def Getdata():
    while True:
        try:
            listMatch = []
            request = requests.get("https://2kooralive.live-kooora.com/")
            soup = BeautifulSoup(request.text, 'html.parser')
            for index,match in enumerate(soup.find_all("div",{"class":"match-container"})):
                linkVideo = match.find("a").get("href")
                playerOne = match.find("div",{"class":"right-team"})
                playerOne_img = playerOne.select("img")[0].get("data-img")
                playerOne_Name = playerOne.find("div",{"class":"team-name"}).text
                matchcenter = match.find("div",{"class":"match-center"})
                reslut = matchcenter.find("div",{"id":"result"}).text
                dateEnd = matchcenter.find("div",{"class":"date"}).get("data-start")
                matchinfo = match.find("div",{"class":"match-info"}).select("ul")[0].select("li")[1].select("span")[0].text
                playerTwo = match.find("div",{"class":"left-team"})
                playerTwo_img = playerTwo.select("img")[0].get("data-img")
                playerTwo_Name = playerTwo.find("div",{"class":"team-name"}).text
                if not str(linkVideo).startswith("#"):
                    getUrlIframe = requests.get(linkVideo)
                    soupIframe = BeautifulSoup(getUrlIframe.text, 'html.parser')
                    iframe = soupIframe.find("iframe",{"class":"video-iframe"}).get("src")
                else:
                    iframe = None
                
                dataRetrun = {
                    "id":index,
                    "linkVideo":iframe,
                    "PlayerOneImage":shrinkImg(playerOne_img),
                    "PlayerTwoImage":shrinkImg(playerTwo_img),
                    "PlayerOneName":playerOne_Name,
                    "PlayerTwoName":playerTwo_Name,
                    "Result":reslut,
                    "StatusMatch":dateEnd,
                    "channel":matchinfo
                }
                
                listMatch.append(dataRetrun)
            LastList.clear
            LastList.append(listMatch)
        except Exception as e:
            pass
        sleep(30)


threading.Thread(target=Getdata, daemon=True).start()



@app.get("/dataMatch")
async def get_data():
    return LastList[0]


def shrinkImg(urlimg):
    url ="https://api.tinify.com/shrink"
    headers = {
        "Host": "api.tinify.com",
        "Authorization": "Basic c1hUekdtWVg1V3dsekhtVmNIOVQ5MHJmTTkwUVpEdG4=",
        "Content-Type": "application/json"
    }
    data = '{"source": {"url": "'+f"{urlimg}"+'"}}'
    return requests.post(url,data=data,headers=headers).json()["output"]["url"]