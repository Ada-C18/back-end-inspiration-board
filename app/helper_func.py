from flask import make_response, abort
import os
import requests

def get_validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model



def send_message_to_slack(task):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API")

    bot_params = {
        "channel": "hungry-coders",
        "text": f"Someone just created a new card"
    }

    requests.post(PATH, data=bot_params, headers={"Authorization": SLACK_API_KEY})