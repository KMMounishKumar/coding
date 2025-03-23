# News Summarization and Text-to-Speech Application

## Overview

This application extracts news articles based on a specified company name, performs sentiment analysis on the articles, and generates a text-to-speech (TTS) audio summary in Hindi. The application is built using Flask for the backend and Streamlit for the frontend, leveraging Hugging Face's Transformers library for sentiment analysis.

## Features

- **News Extraction**: Fetches the latest news articles related to a specified company.
- **Sentiment Analysis**: Analyzes the sentiment of the extracted articles (positive, negative, neutral).
- **Text-to-Speech**: Converts the summarized articles into Hindi audio.
- **User -Friendly Interface**: Built with Streamlit for easy interaction.

## Technologies Used

- Python 3.10
- Flask
- Streamlit
- BeautifulSoup
- Requests
- Pandas
- Transformers
- gTTS (Google Text-to-Speech)
- Nginx (for deployment)

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Clone the Repository
##Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
##Install Dependencies
pip install -r requirements.txt
##Usage
Running the Application Locally
#Start the Flask API:
python api.py
#Start the Streamlit App: (In another terminal)
streamlit run app.py
###Using the Application
Enter the name of the company you want to fetch news for.
Click on "Fetch News" to retrieve articles and their sentiments.
Click on "Generate TTS" to convert the summaries into Hindi audio.


