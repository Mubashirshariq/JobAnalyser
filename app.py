from flask import Flask, request, render_template
import json
from firecrawl import FirecrawlApp
import google.generativeai as genai
import markdown
import os
from dotenv import load_dotenv
import logging

load_dotenv()
app = Flask(__name__)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')

API_KEY = os.getenv('FIRECRAWL_API_KEY')
firecrawl_app = FirecrawlApp(api_key=API_KEY)
print(f"Raw API Key: {repr(API_KEY)}")

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_job_role_percentages(content):
    job_roles_text = f"Based on the content below, estimate the percentages for the various job roles mentioned. If specific percentages aren't given, make an educated guess based on the context. It's okay if the estimates are rough or hypothetical:\n{content}"
    
    try:
        response = model.generate_content(job_roles_text)
        percentages_text = response.text
    except Exception as e:
        logging.error("Error in generating content with Gemini: %s", e)
        return "An error occurred while generating content."

    return markdown.markdown(percentages_text)

@app.route('/', methods=['GET', 'POST'])
def index():
    percentages_html = None
    job_role = None

    if request.method == 'POST':
        url = request.form['url']
        logging.info("URL received: %s", url)
        try:
            scraped_content = firecrawl_app.scrape_url(url=url, params={"pageOptions": {"onlyMainContent": True}})

            percentages_html = get_job_role_percentages(scraped_content)
            logging.info("Job Role Percentages: %s", percentages_html)
        except Exception as e:
            logging.error("Error in scraping or processing the URL: %s", e)
            percentages_html = "An error occurred: " + str(e)

    return render_template('index.html', percentages_html=percentages_html, job_role=job_role)

if __name__ == '__main__':
    app.run(debug=True)
