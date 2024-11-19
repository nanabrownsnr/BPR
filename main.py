import streamlit as st
import pandas as pd

from utilities import create_excel_report,process_data

from linkedin import scrape_linkedin
from twitter import scrape_twitter
from reddit import scrape_reddit




st.title("Product Pulse Analyzer")

keyword = st.text_input("Enter keyword:")
platforms = st.multiselect("Select platforms:", ["Twitter", "Linkedin", "Reddit"])
categories = st.text_input("Enter the categories you want to use to organize your comments","Other", "Efficacy", "Safety", "Ease of Use","Durability")
twitter_results=[]
linkedin_results=[]
reddit_results=[]

if st.button("Generate Daily report"):
    if "Twitter" in platforms:
        twitter_results = scrape_twitter(keyword)
    if "Linkedin" in platforms:
        linkedin_results =scrape_linkedin(keyword)
    if "Reddit" in platforms:
        reddit_results = scrape_reddit(keyword)
    
    processed_twitter_results = process_data("Twitter",twitter_results,categories)
    processed_linkedin_results = process_data("LinkedIn",linkedin_results,categories)
    processed_reddit_results = process_data("Reddit",reddit_results,categories)
    results= processed_twitter_results + processed_linkedin_results + processed_reddit_results
    file = create_excel_report(results)
    st.download_button("Download Report", data=file, file_name="results.xlsx")