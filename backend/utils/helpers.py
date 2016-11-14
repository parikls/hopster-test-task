import json


def json_response(handler, data={}, status=None):
    """
    json response to use inside handlers
    :param handler: `webapp2.RequestHandler`
    :param data: dict
    :param status: int
    """
    handler.response.headers["Content-Type"] = "application/json"
    handler.response.status = status
    handler.response.write(json.dumps(data))
