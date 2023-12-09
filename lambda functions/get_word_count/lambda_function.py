import requests
from bs4 import BeautifulSoup
import json
import re

def lambda_handler(event, context):
    try: 
        if "body" not in event or event["body"] is None:
            raise Exception("event has no body")
        
        body = json.loads(event["body"]) # parse the json
        
        if "url" not in body:
            raise Exception("event has a body but no url")

        url = body["url"]

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text from the HTML
            text = soup.get_text()

            # Use regex to split the text into words
            words = re.findall(r'\b\w+\b', text)

            # Count the number of words
            word_count = len(words)

            # returns total number of words
            return {
                'statusCode': 200,
                'body': json.dumps(word_count)
            }
        
        else:
            raise Exception(f"Failed to retrieve content from {url}. Status code: {response.status_code}")

    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
            'statusCode': 400,
            'body': json.dumps(str(err))
        }