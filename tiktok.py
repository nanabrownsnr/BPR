import requests

def scrape_tiktok(keyword):
    results = [
    {
        "text": "This is a positive review.",
        "sentiment": 0.8,
        "link": "https://example.com/review1"
    },
    {
        "text": "This is a negative review.",
        "sentiment": -0.6,
        "link": "https://example.com/review2"
    },
    ]
    print(results)
    return results
