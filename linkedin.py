import requests
import json

# from python_decouple import config

rapidapi_api_key = "da90478b31msh812ee13e13f28e3p11a732jsna744fe4675ae"

def scrape_linkedin(keyword):
    
    item_texts =[]
    try:
        url = "https://linkedin-data-api.p.rapidapi.com/search-posts-by-hashtag"

        payload = {
            "hashtag": f"{keyword}",
            "sortBy": "REV_CHRON",
            "start": "0",
            "paginationToken": ""
        }
        headers = {
            "x-rapidapi-key": rapidapi_api_key,
            "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com",
            "Content-Type": "application/json"
        }
    
        response = requests.post(url, json=payload, headers=headers)
        # # print(response.json())
        # print(response.text)
        if response.status_code == 200:
            data = response.json()
            items = data['data']['items']
            if items:
                for item in items:
                    item_texts.append(item['text'])
                # Gives only text as intended 
                # print(item_texts)
                # Gives all info
                # print(items)
            else:
                print(f"Error: linkedin list is empty")
        else:
            print(f"Error: linkedin API request failed with status code {response.status_code}")
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as e:
        print(f"Error obtaining linkedin posts: {e}")
        
    return item_texts



# # Test Usage
# post_texts = scrape_linkedin("Haaland")
