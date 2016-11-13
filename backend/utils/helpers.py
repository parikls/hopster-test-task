import json


def json_response(handler, data={}, status=None):

    handler.response.headers["Content-Type"] = "application/json"
    handler.response.status = status
    handler.response.write(json.dumps(data))
