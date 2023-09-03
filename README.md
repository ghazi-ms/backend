# News scraper App
## Overview

    This project is a web application that aggregates news articles from different sources and extracts relevant information, 
    including location data, from these articles.
    The application is built using Python, Flask, and various libraries for web scraping and natural language processing.
## Features

    News Aggregation: The app collects news articles from multiple sources, currently supporting "royanews.tv" and "alghad.com" RSS feeds.

    Text Analysis: It performs text analysis on the article content to identify important keywords and topics.

    Location Extraction: The app extracts location information from the articles, providing geographical coordinates for each news item.

    Web Scraping: It utilizes web scraping techniques to fetch and extract article content from the source websites.

## Technologies Used

- `Python`
- `Flask`
- `BeautifulSoup` (for web scraping)
- `Requests` (for making HTTP requests)
- `Pandas` (for data manipulation)
- `Feedparser` (for parsing RSS feeds)
- `Hugging Face Transformers API` (for text analysis)
- `Google Maps Geocoding API` (for location information)

## Usage
    1. After downloading, get the needed dependencies and run the App.

    2. Access the web app in your web browser at http://localhost:5000/ after installation.

    3. The app will automatically fetch news articles containing specific keywords from the configured sources.

    4. It will extract location information from these articles and provide you with a list of news items with geographical coordinates.

    5. You can customize the keywords and news sources by modifying the code in the app.py file.

    6. The extracted data will be shown in the browser as a JSON formatted data.
# Note

    This app was developed as a part of my graduation project. Some of the API keys included in the code won't be functional.
    You will need to replace them with your own valid API keys for full functionality.
