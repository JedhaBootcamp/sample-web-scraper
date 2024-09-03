import requests
from bs4 import BeautifulSoup
from datetime import datetime 
from lxml import html 
import pandas as pd


def fetch_latest_post(url="https://www.jedha.co/blog"):
    response = requests.get(url)
    
    tree = html.fromstring(response.content)

    # Latest posts are at: /html/body/div[2]/div/div[2]/div
    content= tree.xpath("/html/body/div[2]/div/div[2]")

    extract_content=[]
    for title in content: 
        title_list=title.xpath(".//*[contains(@class, 'h6')]")    
        parsed_titles=[title.text_content() for title in title_list]
    
    return parsed_titles


def log_posts(posts):
    now = datetime.now()
    df = pd.DataFrame({"Posts": posts, "Extracted_Date":[now for now in range(len(posts))]})
    df.to_csv(f"./posts/posts-{now}.csv", index=False)
    return "Logged latest posts"


if __name__ == "__main__":
    
    latest_posts = fetch_latest_post()
    log_posts(latest_posts)
    print(f"Logged {len(latest_posts)} Articles.")