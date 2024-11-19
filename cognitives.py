from transformers import pipeline
import torch
import requests
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import json
import streamlit as st

@st.cache_resource
def load_models():
    # Model 1
    emotion_classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    # Model 2
    model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, trust_remote_code=True)
    sentiment_classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    # Model 3
    category_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

    # Model 4 -identify source language
    language_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

    # Model 5 -translate from source language to english
    language_transformer = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
    return emotion_classifier,sentiment_classifier,category_classifier,language_classifier,language_transformer



emotion_classifier,sentiment_classifier,category_classifier,language_classifier,language_transformer = load_models()


def determine_translation(text):
    try:
        response1 = language_classifier(text)
        response2 =language_transformer(text, response1)
        result = response2.json()
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as e:
        print(f"Error processing emotion: {e}")
        result = "Failed"
    return result

def determine_emotion(text):
    try:
        response = emotion_classifier(text)
        if response and len(response) > 0:
            result = response[0][0]['label']
            # print("emotion result:", result)
        else:
            raise ValueError("Invalid JSON response format")
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as e:
        print(f"Error processing emotion: {e}")
        result = "Failed"
    return result

def determine_sentiment(text):
    try:
        response = sentiment_classifier(text)
        if response and len(response) > 0 and len(response[0]) > 0:
            result = response[0]['label']
            # print("sentiment result:", result)
        else:
            raise ValueError("Invalid JSON response format")
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as e:
        print(f"Error processing emotion: {e}")
        result = "Failed"
    return result

def determine_category(text,categories):
    try:
        response = category_classifier(text,categories)
        if response and len(response) > 0:
            result = response['labels'][0]
            # print("category result:", result)
        else:
            raise ValueError("Invalid JSON response format")
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as e:
        print(f"Error processing emotion: {e}")
        result = "Failed"
    return result



# # Test Usage
# text = "Covid cases are increasing fast!"
# result1 = emotion_classifier(text)
# result2 = sentiment_classifier(text)
# 
# result3 = category_classifier(text,categories)
# print(result1[0][0]['label'])
# print(result2[0]['label'])
# print(result3['labels'][0])

# print("\nTest 2")
# print(determine_sentiment(text))
# print(determine_emotion(text))
# print(determine_category(text,categories))