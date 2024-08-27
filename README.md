# Job Role Percentage Extractor

This project is a Flask web application that extracts and estimates job role percentages from web content. The application uses the Gemini model from Google Generative AI for natural language processing and the Firecrawl service for web scraping.

## Features

- **Web Scraping**:Uses FireCrawl for  Scraping  content from a provided  website URL containing data related jobs  to extract the main content.
- **NLP Analysis**: Uses Google Generative AI's Gemini model to estimate the percentages of job roles mentioned in the content.
- **Markdown Rendering**: Converts the text output into HTML for display on the web interface.

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- A Google Generative AI API key
- A Firecrawl API key


