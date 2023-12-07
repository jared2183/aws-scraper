import requests
from bs4 import BeautifulSoup
import re
import json

def get_word_count(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content from the HTML
        text_content = soup.get_text()

        # Use regular expression to find words (assuming words are separated by spaces)
        words = re.findall(r'\b\w+\b', text_content)

        # Count the number of words
        word_count = len(words)

        print(f"Word count of {url}: {word_count} words")
    else:
        raise Exception(f"Failed to retrieve content from {url}. Status code: {response.status_code}")

# Example usage:
url_to_count_words = 'https://example.com'
get_word_count(url_to_count_words)