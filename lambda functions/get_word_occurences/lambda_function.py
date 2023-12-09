import json
import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    try:
        if "body" not in event or event["body"] is None:
            raise Exception("event has no body")
            
        # Parse the JSON body of the request
        request_body = json.loads(event['body'])

        # Extract target_word and url from the request body
        target_word = event['pathParameters']['target_word']
        url = request_body['url']

        # Fetch HTML content from the URL
        response = requests.get(url)
        html_content = response.text

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find occurrences of the target word in the HTML text
        word_count = soup.text.lower().count(target_word.lower())

        # Return the result
        return {
            'statusCode': 200,
            'body': json.dumps({'result': f'The word \"{target_word}\" occurs {word_count} times.'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error: {str(e)}'})
        }
