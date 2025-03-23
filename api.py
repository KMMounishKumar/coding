from flask import Flask, request, jsonify
from utils import extract_news, analyze_sentiment, comparative_analysis, text_to_speech_hindi

app = Flask(__name__)  

@app.route('/fetch_news', methods=['POST'])
def fetch_news():
    try:
        data = request.json
        print(f"🔍 Received Data: {data}")  #  Debugging Step

        company_name = data.get('company_name')
        if not company_name or not company_name.strip():
            return jsonify({"error": " Company name is required"}), 400

        articles = extract_news(company_name)
        if isinstance(articles, dict) and "error" in articles:
            return jsonify(articles), 500  

        sentiments = []
        for article in articles:
            sentiment = analyze_sentiment(article['summary'])
            sentiment_label = sentiment[0]['label'].lower() if sentiment else "neutral"
            sentiments.append({'label': sentiment_label})
            article['sentiment'] = sentiment_label

        sentiment_counts = comparative_analysis(sentiments)

        return jsonify({
            'company': company_name,
            'articles': articles,
            'sentiment_distribution': sentiment_counts
        })

    except Exception as e:
        return jsonify({"error": f" Unexpected error: {str(e)}"}), 500

@app.route('/generate_tts', methods=['POST'])
def generate_tts():
    try:
        data = request.json
        text = data.get('text')

        if not text or not text.strip():
            return jsonify({"error": " Text input is required"}), 400

        audio_file = text_to_speech_hindi(text)
        if not audio_file:
            return jsonify({"error": " Failed to generate TTS"}), 500

        return jsonify({'audio_file': audio_file})

    except Exception as e:
        return jsonify({"error": f" Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
