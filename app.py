import streamlit as st
import requests

st.set_page_config(page_title="News Summarization & Sentiment Analysis", layout="centered")
st.title("📰 News Summarization & Sentiment Analysis 🎤")

#  User input for company name
company_name = st.text_input("Enter Company Name:")

# Backend API URL 
BACKEND_URL = "https://4347-2409-4071-e14-c9c8-b4db-b21d-acce-90c.ngrok-free.app"

if st.button("Fetch News"):
    if not company_name.strip():
        st.error("Please enter a company name!")
    else:
        try:
            with st.spinner("Fetching latest news... 📡"):
                response = requests.post(f"{BACKEND_URL}/fetch_news", json={'company_name': company_name})
            
            if response.status_code == 200:
                data = response.json()
                st.session_state["news_data"] = data  
            else:
                st.error(f" Error fetching news! Status Code: {response.status_code}")
                st.stop()  

            if "error" in data:
                st.error(f" {data['error']}")
            else:
                st.write(f"## 📝 Articles on {company_name.capitalize()}")
                for idx, article in enumerate(data.get('articles', []), start=1):
                    with st.expander(f"📰 {idx}. {article['title']}"):
                        st.markdown(f"📄 **Summary:** {article['summary']}")
                        st.markdown(f"📊 **Sentiment:** `{article['sentiment'].capitalize()}`")
                        st.markdown(f"[🔗 Read More]({article['url']})")

                # Show sentiment distribution
                st.write("## 📊 Sentiment Distribution")
                st.bar_chart(data['sentiment_distribution'])

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend! Is the Flask server running?")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

# Generate Hindi TTS from summaries
if st.button("Generate Hindi TTS"):
    if "news_data" in st.session_state and "articles" in st.session_state["news_data"]:
        try:
            text = " ".join([article['summary'] for article in st.session_state["news_data"]["articles"]])
            if not text.strip():
                st.error(" No text available for TTS!")
            else:
                with st.spinner("Generating Hindi audio... 🔊"):
                    response = requests.post(f"{BACKEND_URL}/generate_tts", json={'text': text})
                    tts_data = response.json()

                if "error" in tts_data:
                    st.error(f" Error: {tts_data['error']}")
                else:
                    st.success("🎧 Hindi TTS generated successfully! Click below to play:")
                    st.audio(tts_data['audio_file'], format="audio/mp3")

        except requests.exceptions.ConnectionError:
            st.error(" Could not connect to the backend! Is the Flask server running?")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
    else:
        st.error(" Please fetch news before generating TTS!")
