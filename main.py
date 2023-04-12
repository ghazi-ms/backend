import random
from flask import Flask, jsonify
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import feedparser


pd.set_option('display.max_colwidth', 500)
api_key = "AIzaSyAKY_4kNJ0xHBgVCE6k9ZgSX-njXno1BTQ"
API_URL = "https://api-inference.huggingface.co/models/CAMeL-Lab/bert-base-arabic-camelbert-msa-ner"
headers = {"Authorization": "Bearer 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"}

app = Flask(__name__)


@app.route('/')

# start of the code

def start():
    the_word = ["الأعاصير", "إطلاق نار", "زلزال", "حوادث", "زلازل", "حريق", "إرهاب", "الجرائم", "بحادثي", "وفاتان",
            "حرب", "إصابات", "بانفجار"]
    Feed = feedparser.parse('https://www.royanews.tv/rss')  # connect to royas rss

    DataList = []  # the list that will have the initial data of type news
    ImportnatnList = []

    for i in Feed.entries:
        # take every element in the list and cut the title and link
        t = str(i).split("author")[3]
        t = t.split("title")[2]
        links = t.split("base")[1]
        links = links.split("href")[1]
        links = links.split("}")[0]
        links = links.split("'")[2]
        title = t.split("value")[1]
        title = title.split("}")[0]

        title = title.split("'")[2]
        DataList.append(news(title, links))  # add the title and link to a new news object

    for data in DataList:
        for word in the_word:
            if data.GetTitle().__contains__(
                    word):  # if the data retrived from the list of the object news titles has any word of the keywords
                tmp_data = news(data.title, data.link)
                if tmp_data not in ImportnatnList:
                    ImportnatnList.append(news(data.title, data.link))  # add the object to the filterd list

    if ImportnatnList:  # if there is a filtered list then call the extractor, and it's not empty
        extract(ImportnatnList)
    theJsonlist = {}

    for newsObject in ImportnatnList:
        locations = newsObject.Getlocation()  # gets the location of the news
        if locations != "":
            locations = locations.split(',')  # the data is like amman,zaraqa,psut, so it splits the locations
            locations = list(dict.fromkeys(locations))
            locations.remove('')
            for location in locations:
                newsObject.SetPoints(get_boundary_coordinates(location))  # extract the coordinates of the location word
        theJsonlist[str(random.randrange(1, 55))] = newsObject.getIntoList()  # turn the objects of news into a json list

    return jsonify(theJsonlist)


def extract(important_list):
        for newsObjectData in important_list:

            url = newsObjectData.GetLink()  # get the objects link (the news link)

            response = requests.get(url) # request the page
            soup = BeautifulSoup(response.content, "html.parser") # open the page

            # find all sections in the HTML
            sections = soup.find_all("section")

            # check if there are at least four sections
            if len(sections) >= 4:
                target_section = sections[4]
                target_section_contents = target_section.get_text()
                target_section_contents = "\n".join(
                    [line.strip() for line in target_section_contents.split("\n") if line.strip()])
                newsObjectData.Setdescription(target_section_contents) # sets the description of the news object

            ExtractLocation(important_list) # calls the extract location to extract the location from the description


def extract_static(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # find all sections in the HTML
        sections = soup.find_all("div", {"class": "article"})

        # check if there are at least two sections

        for data in sections:
            second_section_contents = data.get_text()
            second_section_contents = "\n".join(
                [line.strip() for line in second_section_contents.split("\n") if line.strip()])


def get_boundary_coordinates(place_name):
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={api_key}"
        response = requests.get(geocode_url)
        response_json = response.json()
        results = response_json["results"]
        if len(results) == 0:
            return None
        result = results[0]
        geometry = result["geometry"]
        bounds = geometry.get("bounds")
        if bounds is None:
            viewport = geometry["viewport"]
            southwest = viewport["southwest"]
            northeast = viewport["northeast"]
            boundary_coordinates = [(southwest["lat"], southwest["lng"]), (northeast["lat"], northeast["lng"])]
        else:
            southwest = bounds["southwest"]
            northeast = bounds["northeast"]
            boundary_coordinates = [(southwest["lat"], southwest["lng"]), (northeast["lat"], northeast["lng"]),
                                    (northeast["lat"], southwest["lng"]), (southwest["lat"], northeast["lng"])]
        return boundary_coordinates

def GetDataAndDescription(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        estimatedTime = 0
        if 'estimated_time' in response:
            estimatedTime = response['estimated_time']

        if estimatedTime > 0:

            time.sleep(estimatedTime)
            response = requests.post(API_URL, headers=headers, json=payload)

        return response.json()

def ExtractLocation(important_list):
        theLocation = ""

        for newsData in important_list:
            if newsData.Getdescription() != '': # check if there is a description
                response = GetDataAndDescription(newsData.Getdescription()) # send the description to the function

                for item in response:
                    if isinstance(item, dict) and 'entity_group' in item:
                        if item['entity_group'] == 'LOC':
                            if item['entity_group'] == 'LOC':
                                theLocation = theLocation + item['word'] + "," # append the extracted locations

            if theLocation != "":
                newsData.SetLocation(theLocation) # add the list of locations
                newsData.SettimeStamp(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())) # give the news a time stamp
            theLocation = ""



class news:

    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.description = ""
        self.location = ""
        self.timeStamp = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
        self.points=[]
    def __str__(self):
        return "the title is :" + self.title + ",\n the link is:" + self.link + "\n the Description\n" + self.description + "\n the loc:" + self.location + "\n the time:" + self.timeStamp

    def __eq__(self, other):
        if isinstance(other,self.__class__):
            return self.title == other.title
        return False
    def getIntoList(self):
        return {
        "id": 'id'+str(random.randrange(1,99999999)),
        "title": self.title,
        "description": self.description,
        "Coordinates": self.points,
        "Locations":self.location,
        "timeStamp": self.timeStamp
        }
    def SetPoints(self,pointss):
        self.points=pointss
    def GetTitle(self):
        return str(self.title)

    def GetLink(self):
        return str(self.link)

    def Getlocation(self):
        return str(self.location)

    def SetLocation(self, Loc):
        self.location = Loc

    def GettimeStamp(self):
        return str(self.timeStamp)

    def SettimeStamp(self, timestamp):
        self.timeStamp = timestamp

    def Setdescription(self, description):
        self.description = description

    def Getdescription(self):
        return str(self.description)

if __name__ == '__main__':
    app.run(debug=True)