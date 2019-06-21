import requests
import bs4
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
#from uszipcode import SearchEngine
from pymongo import MongoClient
from flask_pymongo import PyMongo


def scrapeIndeed(job_title):

    job_titles = []
    company_names = []
    locations = []
    salaries = []
    link_list = []

    url = f'https://www.indeed.com/jobs?q={job_title}&limit=50'

    
    def scrapeData(class_str, list_name):
        element = soup.find_all(class_=class_str)
        for i in element:
            list_name.append(i.text.strip())

    def scrapeSalary(num, list_name):
        salary_tags = soup.find_all(class_='row')
        for i in range(len(salary_tags)):
            try:
                salary = salary_tags[i].find(class_='salary').text.strip()
                list_name.append(salary)
            except:
                list_name.append("No Salary Info Provided")

    def scrapeLink(list_name):
        frontend = 'https://www.indeed.com/'
        links = soup.find_all('div', class_='title')
        for link in links:
            backend = link.find('a')['href']
            list_name.append(frontend+backend)
    
    def getZip(str, zipList):
        if str.isdigit():
            zipList.append(str)
        else:
            try:
                search = SearchEngine(simple_zipcode=True)
                city_state_str = str.split(', ')
                city_state = search.by_city_and_state(city_state_str[0], city_state_str[1])
                zipList.append(city_state[0].zipcode)
            except:
                zipList.append("None")
                print(f"No City, State info found for {str}")

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    scrapeData('title', job_titles)
    scrapeData('company', company_names)
    scrapeData('location', locations)
    num = len(job_titles)
    scrapeSalary(num, salaries)
    scrapeLink(link_list)

    browser.quit()


    def hasZip(inputString):
        if any(char.isdigit() for char in inputString):
            #return inputString[-5:]
            return "".join(filter(lambda x: x.isdigit(), inputString))
        else:
            return inputString


    loc_list = []
    for i in locations:
        loc_list.append(hasZip(i))

    #zip_list = []
    # for i in loc_list:
    #     getZip(i, zip_list)

    # def getCoord(str, coordList, cityList):
    #     search = SearchEngine(simple_zipcode=True)
    #     if str.isdigit():
    #         try:
    #             zipcode = search.by_zipcode(str)
    #             coords = [zipcode.lat, zipcode.lng]
    #             coordList.append(coords)
    #             cityList.append(zipcode.post_office_city)
    #         except:
    #             coordList.append(["None", "None"])
    #             cityList.append("None")
    #             print(f"No Results Found for Zip {str}")
    #     else:
    #         coordList.append(["None", "None"])
    #         cityList.append(str)
    
    

    # coord_list = []
    # city_list = []

    # for i in zip_list[0:search_limit]:
    #     getCoord(i, coord_list, city_list)

    search_limit = 50
    job_list = []

    for i in range(search_limit):
        job_dict = {}
        job_dict['Title'] = job_titles[i]
        job_dict['Company'] = company_names[i]
        job_dict["Locations"] = loc_list[i]
        #job_dict['Location'] = city_list[i]
        #job_dict["Coordinates"] = coord_list[i]
        job_dict["Salary_Info"] = salaries[i]
        job_dict['Link'] = link_list[i]
        job_list.append(job_dict)

    # for i in job_list:
    #     if "None" in str(i["Coordinates"]):
    #         job_list.remove(i)

    # conn = 'mongodb://localhost:27017'
    # client = MongoClient(conn)
    # db = client['job_search_db']

    # db.search_results.drop()

    # col = db['search_results']

    # for x in job_list:
    #     col.insert_one(x)
    
    return(job_list)