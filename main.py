from typing import Optional




from typing import Union

import requests
from bs4 import BeautifulSoup
app = FastAPI()





@app.get("/dataMatch")
def get_data():
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
                "PlayerOneImage":playerOne_img,
                "PlayerTwoImage":playerTwo_img,
                "PlayerOneName":playerOne_Name,
                "PlayerTwoName":playerTwo_Name,
                "Result":reslut,
                "StatusMatch":dateEnd,
                "channel":matchinfo
            }
            listMatch.append(dataRetrun)
        return listMatch
    except Exception as e:
        return {"message":e}
