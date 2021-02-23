import requests
import sys


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    gateway_socket = "gateway.openfaas:8080"
    remote_fun = "/function/sentiment-analysis"

    data = req.encode("utf-8")

    r = requests.get("http://" + gateway_socket + remote_fun, data=data)

    if r.status_code != 200:
        sys.exit(f"Error calling func, expected: 200, got: {r.status_code}")

    result = r.json()

    if result["polarity"] > 0.45:
        return "Positive comment"

    elif result["polarity"] <= 0.45 and result["polarity"] > -0.2:
        return "Neutral comment"

    else:
        return "Negative comment"
