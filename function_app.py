import azure.functions as func
import logging
import os
import json
import re
import requests
import openai

app = func.FunctionApp()

# Load keys from environment variables (set in local.settings.json)
openai.api_key = os.environ.get("OPENAI_API_KEY")
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

def get_tweet_id(url):
    match = re.search(r'/status/(\d+)', url)
    if not match:
        raise Exception("Invalid Tweet URL")
    return match.group(1)

def get_tweet_text(tweet_ids: list):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {"ids": tweet_ids, "tweet.fields": "author_id"}
    res = requests.get(url, headers=headers, params=params)
    data = res.json()
    print(data)
    return data['data']['text']

def generate_flashcard(tweet_text, tweet_url):
    prompt = f"""
    Create a flashcard from this tweet.

    Tweet: "{tweet_text}"

    Front: (beginning of the tweet, choose properly)
    Back: (rest of the tweet)

    Return it as Front: ... and Back: ...

    Make sure to not modify the tweet text.
    """

    response = openai.responses.create(
        model="gpt-4.1",
        input=[{"role": "user", "content": prompt}]
    )

    content = response.output_text
    match = re.search(r'Front:(.*?)Back:(.*)', content, re.DOTALL)
    front = match.group(1).strip()
    back = match.group(2).strip() + f"\n\n {tweet_url}"
    return front, back

@app.route(route="generateFlashcard", auth_level=func.AuthLevel.FUNCTION)
def generateFlashcard(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing flashcard generation")

    try:
        tweet_url = req.params.get('url')
        if not tweet_url:
            req_body = req.get_json()
            tweet_url = req_body.get("url")

        if not tweet_url:
            return func.HttpResponse("Missing tweet URL", status_code=400)

        tweet_id = get_tweet_id(tweet_url)
        tweet_text = get_tweet_text(tweet_id)
        # tweet_text = "How you feel about yourself is how you feel about the world"
        front, back = generate_flashcard(tweet_text, tweet_url)

        return func.HttpResponse(
            json.dumps({"front": front, "back": back}),
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("Error generating flashcard")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
