from textblob import TextBlob


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    blob = TextBlob(req)

    res = {'polarity': 0}

    for sentence in blob.sentences:
        res['polarity'] += sentence.sentiment.polarity

    return {'polarity': res['polarity']}
