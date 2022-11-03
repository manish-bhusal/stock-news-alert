from datetime import datetime, timedelta
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API")
NEWS_API_KEY = os.getenv("NEWS_API")

account_sid = "ACc339a84cef9749acc4c44f8e0522ff1b"
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)


tesla_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_API_KEY
}
yesterday = (datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d")
the_day_before_yesterday = (
    datetime.today()-timedelta(days=2)).strftime("%Y-%m-%d")
response_alpha = requests.get(
    STOCK_ENDPOINT, params=tesla_params)
response_alpha.raise_for_status()
tesla_data = response_alpha.json()
yesterday_closing_price = float(tesla_data.get(
    "Time Series (Daily)").get(yesterday).get("4. close"))
the_day_before_yesterday_closing_price = float(tesla_data.get(
    "Time Series (Daily)").get(the_day_before_yesterday).get("4. close"))

print(yesterday_closing_price)
print(the_day_before_yesterday_closing_price)


difference = yesterday_closing_price - the_day_before_yesterday_closing_price
up_dowm = None
if difference > 0:
    up_dowm = "🔺"
else:
    up_dowm = "🔻"

diff_percent = round((difference/yesterday_closing_price)*100)
print(diff_percent)
if abs(diff_percent) > 4:
    news_params = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    response_news = requests.get(
        NEWS_ENDPOINT, params=news_params)

    response_news.raise_for_status()
    news_data = response_news.json().get("articles")

    three_articles = news_data[:3]
    formatted_articles = [
        f"{STOCK}: {up_dowm}{diff_percent}%\nHeadline: {article.get('title')}.\nBrief: {article.get('description')} " for article in three_articles]

    for article in formatted_articles:

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=article,
            to=f'whatsapp:{os.getenv("MY_NUMBER")}'
        )
        print(message.sid)
