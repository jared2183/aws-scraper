import requests
from bs4 import BeautifulSoup
import json

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

            # Find all anchor tags (a) with href attribute
            links_html = soup.find_all('a', href=True)

            # Extract and print the href attribute of each link
            links = []
            for link in links_html:
                # skips link if it is not a full URL
                if not link['href'].startswith('http'):
                    continue
                # adds link URL to links list
                print(link['href'])
                links.append(link['href'])

            # returns list of links
            return {
                'statusCode': 200,
                'body': json.dumps(links)
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