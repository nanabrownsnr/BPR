import requests
from decouple import config
import json
import datetime
# rapidapi_api_key = config('RAPIDAPI_API_KEY')
rapidapi_api_key = "da90478b31msh812ee13e13f28e3p11a732jsna744fe4675ae"
now = datetime.datetime.now().strftime("%Y-%m-%d")


def scrape_twitter(keyword):
    
    item_texts =[]
    try:
        url = "https://twitter154.p.rapidapi.com/search/search"
    
        payload = {
            "query": f"#{keyword}",
            "limit": 50,
            "section": "top",
            "language": "en",
            "min_likes": 20,
            "min_retweets": 20,
            "start_date": now,
        }
        headers = {
            "x-rapidapi-key": rapidapi_api_key,
            "x-rapidapi-host": "twitter154.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            items = data['results']
            if items:
                for item in items:
                    item_texts.append(item['text'])
                # Gives only text as intended 
                # print(item_texts)
            else:
                print(f"Error: linkedin list is empty")
        else:
            print(f"Error: twitter API request failed with status code {response.status_code}")
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as e:
        print(f"Error obtaining twitter posts: {e}")
        
    return item_texts



# # Test Usage
# post_texts = scrape_twitter("Haaland")