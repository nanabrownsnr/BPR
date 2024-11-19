import requests
import json

rapidapi_api_key = "da90478b31msh812ee13e13f28e3p11a732jsna744fe4675ae"


def scrape_reddit(keyword):
    item_texts = []
    try:
        url = "https://reddit-scraper2.p.rapidapi.com/search_posts"

        querystring = {"query": f"{keyword}","sort": "TOP", "time": "all", "nsfw": "1"}

        headers = {
            "x-rapidapi-key": rapidapi_api_key,
            "x-rapidapi-host": "reddit-scraper2.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            items = data['data']
            next_page_token = data['pageInfo']['endCursor']
            if items:
                for item in items:
                    item_texts.append(item['title'])

                querystring_2 = {"query": f"{keyword}","sort": "TOP", "time": "all", "nsfw": "1","cursor":next_page_token}
                response_2 = requests.get(url, headers=headers, params=querystring_2)
                if response_2.status_code == 200:
                    data_2 = response_2.json()
                    items_2 = data_2['data']
                    for item_2 in items_2:
                        item_texts.append(item_2['title'])
                        
                    # print(item_texts)
            else: 
                print(f"Error: reddit list is empty")
                
        else:
            print(f"Error: reddit API request failed with status code {
                  response.status_code}")
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as e:
        print(f"Error obtaining reddit posts: {e}")

    return item_texts


# # Test Usage
# post_texts = scrape_reddit("Haaland")

