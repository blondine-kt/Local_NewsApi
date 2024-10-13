import os
# external_api/main.py
from fastapi import FastAPI
from datetime import datetime

import worldnewsapi.configuration
from dotenv import load_dotenv
import requests
import uvicorn
import worldnewsapi
from worldnewsapi.models.get_geo_coordinates200_response import GetGeoCoordinates200Response
from worldnewsapi.models.retrieve_newspaper_front_page200_response import RetrieveNewspaperFrontPage200Response
from worldnewsapi.models.search_news200_response_news_inner import SearchNews200ResponseNewsInner
from worldnewsapi.rest import ApiException
from pprint import pprint
load_dotenv()

app = FastAPI()


    
def get_news(city):

    # configuration = worldnewsapi.configuration(
    #     host = "https://api.worldnewsapi.com"
    # ) 
    #configure date of article
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")

    # Add authorization by using APIKey 
    # load api key from .env file
    #configuration.api_key['api_key'] = os.environ["API_KEY"]
    api_key= os.environ["API_KEY"]
     
     #Configurate news API
    newsapi_configuration = worldnewsapi.Configuration(api_key={'apiKey':api_key})
    
    try: 
        #create news instance to get top news of given location
        newsapi_instance = worldnewsapi.NewsApi(worldnewsapi.ApiClient(newsapi_configuration))

        location = newsapi_instance.get_geo_coordinates(city)


        response = newsapi_instance.search_news(
                text='artificial intelligence',
                location_filter= str(location.latitude)+', '+str(location.longitude)+',30',
                language='en',
                latest_publish_date=formatted_date,
                offset=0,
                number=2
                )
        
        
        for news in response.news:
            
                local_news ={
                    "title": str(news.title),
                    "auteur": str(news.author),
                    "url": str(news.url),
                    "text": str(news.text[:300])+"..."
                }




        print(response)
        

    except worldnewsapi.ApiException as e:
        print("Exception when calling NewsApi->search_news: %s\n" % e)

        local_news ={
                    "title": "NA",
                    "auteur": "NA",
                    "url": "NA",
                    "text": "NA"
                }


    
    return local_news
        

   

@app.get("/news/")

async def get_localnew(city):
    response = get_news(city)

    return response

if __name__=='__main__':
     uvicorn.run(app,'0.0.0.0', port=8035, workers=2)