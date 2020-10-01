import json
import nltk
from textblob import TextBlob


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    finally:
        blob = TextBlob(req)

    res = {'polarity': blob.sentiment.polarity}

    return json.dumps(res)
