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


#function to get city  geocde
def getcity_geocode(city):
    
    url = f"https://api.worldnewsapi.com/geo-coordinates?location={city}"
    api_key = os.environ["API_KEY"]

    headers = {
        'x-api-key': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        geocode = str(data['latitude'])+', '+ str(data['longitude']) +', 20'
        



        return(geocode)
    else:
        return f"Error: {response.status_code}"
    
def get_news():

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

        location = newsapi_instance.get_geo_coordinates('Toronto')


        response = newsapi_instance.search_news(
                text='artificial intelligence',
                location_filter= str(location.latitude)+', '+str(location.longitude)+',30',
                language='en',
                latest_publish_date=formatted_date,
                number=1
                )
        
        json ="{}"
        search_news200_response_news_inner_instance = SearchNews200ResponseNewsInner.from_json(json)
        print(SearchNews200ResponseNewsInner.to_json())
        
        # local_news = {
        #     'title':response['title'],
        #     'author': response['author'],
        #     'url':response['url'],
        #     'image':response['image'],
        #     'text':response['text']
        # }
        print(response)
        return response.model_dump_json()

    except worldnewsapi.ApiException as e:
        print("Exception when calling NewsApi->search_news: %s\n" % e)

   

    

        

   

@app.get("/news")

async def get_localnew():
    response = get_news()

    return response

if __name__=='__main__':
     uvicorn.run(app,'0.0.0.0', port=8035, workers=2)