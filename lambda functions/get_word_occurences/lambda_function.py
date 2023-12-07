import requests
from bs4 import BeautifulSoup

def get_word_occurrences(url, target_word):
    
    
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content from the HTML
        text_content = soup.get_text()

        # Count occurrences of the target word
        word_count = text_content.lower().count(target_word.lower())

        print(f"The word '{target_word}' appears {word_count} times on {url}")
    else:
        raise Exception(f"Failed to retrieve content from {url}. Status code: {response.status_code}")

# Example usage:
url_to_count_word = 'https://example.com'
target_word_to_count = 'example'
get_word_occurrences(url_to_count_word, target_word_to_count)
