from functools import wraps
import simplejson as json


class BoxViewError(Exception):
    def __init__(self, response=None):
        Exception.__init__(self)
        self.status_code = response.status_code

        if response.headers.get('content-type') == 'application/json':
            self.response_json = response.json()
        else:
            self.response_json = '{}'

    def __str__(self):
        self.response_json = json.dumps(
            self.response_json,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

        return "\nHTTP Status: {}\n{}".format(
            self.status_code,
            self.response_json
        )


def raise_for_view_error(func):
    @wraps(func)
    def checked_for_view_error(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            result.raise_for_status()
            return result
        except:
            raise BoxViewError(result)
    return checked_for_view_error
