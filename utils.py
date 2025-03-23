import requests
from transformers import pipeline
from gtts import gTTS
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator  
import torch

#  Initialize sentiment pipeline once 
device = "cuda" if torch.cuda.is_available() else "cpu"
sentiment_pipeline = pipeline("sentiment-analysis", device=0 if device == "cuda" else -1)

#  Extract news using NewsAPI + Web Scraping fallback
def extract_news(company_name):
    API_KEY = "72d6f9c6c3974c959042fe1480016da5"  
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&pageSize=10&apiKey={API_KEY}"

    response = requests.get(url)

    
    if response.status_code != 200:
        return {"error": f"Failed to fetch news. Status Code: {response.status_code}"}

    data = response.json()

    if data.get("status") != "ok":
        return {"error": "API request failed", "status": data.get("status")}

    articles = []
    for article in data.get("articles", [])[:10]:
        summary = article.get("description", "No summary available.")

        # Web Scraping if No Summary Available
        if summary == "No summary available.":
            scraped_summary = scrape_article(article["url"])
            if scraped_summary:
                summary = scraped_summary

        articles.append({
            "title": article.get("title", "No Title"),
            "summary": summary,
            "url": article.get("url", "#")
        })

    return articles

# Web Scraping Function (Fallback)
def scrape_article(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        extracted_text = " ".join([p.get_text() for p in paragraphs[:3]])  #  Extract first 3 paragraphs

        return extracted_text if extracted_text else None
    except Exception:
        return None

# Sentiment Analysis using Hugging Face Transformers
def analyze_sentiment(text):
    if not text.strip():
        return [{"label": "neutral", "score": 0.0}]

    return sentiment_pipeline(text)

# Sentiment Distribution Calculation
def comparative_analysis(sentiments):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for sentiment in sentiments:
        label = sentiment['label'].lower()

        if "negative" in label:
            sentiment_counts["Negative"] += 1
        elif "positive" in label:
            sentiment_counts["Positive"] += 1
        else:
            sentiment_counts["Neutral"] += 1  

    return sentiment_counts

#  Convert English Text to Hindi and Generate Speech
def text_to_speech_hindi(text, filename='output.mp3'):
    if not text.strip():
        return None

    try:
        #translate English Text to Hindi using Deep Translator
        translated_text = GoogleTranslator(source='en', target='hi').translate(text)

        if not translated_text.strip(): 
            translated_text = text  

        print(f"🔵 Translated Hindi Text: {translated_text}") 

        # ✅ Convert Translated Text to Speech
        tts = gTTS(text=translated_text, lang='hi', slow=False)
        tts.save(filename)

        return filename
    
    except Exception as e:
        print(f"⚠️ Translation Error: {e}")  
        return None  # return None if translation fails
