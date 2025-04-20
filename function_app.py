import azure.functions as func
import logging
import os
import json
import re
import requests
import openai

app = func.FunctionApp()

openai.api_key = os.environ.get("OPENAI_API_KEY")
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

def get_tweets_ids(urls: list):
    ids = []
    for url in urls:
        match = re.search(r'/status/(\d+)', url)
        if not match:
            raise Exception("Invalid Tweet URL")
        ids.append(match.group(1))
    return ids

def get_tweets(tweet_ids: list):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {"ids": tweet_ids, "tweet.fields": "author_id"}
    res = requests.get(url, headers=headers, params=params)
    data = res.json()
    return data['data']

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
        tweet_urls = req.params.get('urls')
        if not tweet_urls:
            req_body = req.get_json()
            tweet_urls = req_body.get("urls")
        if not tweet_urls:
            return func.HttpResponse("Missing tweet URL", status_code=400)

        tweet_ids = get_tweets_ids(tweet_urls)
        tweets = get_tweets(tweet_ids)
        for url, tweet in zip(tweet_urls, tweets):
            front, back = generate_flashcard(tweet_text=tweet['text'], tweet_url=url)

        return func.HttpResponse(
            json.dumps({"front": front, "back": back}),
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("Error generating flashcard")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
