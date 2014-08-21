import os
import requests
import simplejson as json
import settings as s
from boxviewerror import raise_for_view_error

DOCUMENTS_RESOURCE = '/documents'
SESSIONS_RESOURCE = '/sessions'
VIEW_RESOURCE = '/view'

PROCESSING = 'processing'
DONE = 'done'


def _set_token_from_env():

    box_view_token = os.environ.get('BOX_VIEW_TOKEN')

    if not box_view_token:
        raise ValueError(
            """Calling BoxViewClient() with no arguments requires environment
            variables to be set like this:

            >>> import os
            >>> os.environ['BOX_VIEW_TOKEN'] = YOUR_BOX_VIEW_TOKEN
            """
        )
    return box_view_token


class BoxViewClient(object):
    """A simple wrapper around the Box View API

    Args:
        api_token: A valid box view api token, get one here: bit.ly/boxapikey

    Attributes:

    """

    def __init__(self, api_token=None):

        if not api_token:
            api_token = _set_token_from_env()

        auth_header = {'Authorization': 'Token {}'.format(api_token)}

        self.requests = requests.session()
        self.requests.headers = auth_header
        self.url = s.VIEW_API_URL
        self.upload_url = s.UPLOAD_VIEW_API_URL

    # Core API Methods

    @raise_for_view_error
    def upload_document(self, url):
        """
        """

        resource = '{}{}'.format(self.url, DOCUMENTS_RESOURCE)
        headers = {'Content-type': 'application/json'}
        data = json.dumps({'url': url})

        response = self.requests.post(resource, headers=headers, data=data)

        return response

    @raise_for_view_error
    def multipart_upload_document(self, document):
        """
        """

        resource = '{}{}'.format(self.upload_url, DOCUMENTS_RESOURCE)
        files = {'file': document}

        response = self.requests.post(resource, files=files)

        return response

    @raise_for_view_error
    def get_document(self, document_id):
        """
        """

        resource = '{}{}/{}'.format(
            self.url,
            DOCUMENTS_RESOURCE,
            document_id
        )

        response = self.requests.get(resource)

        return response

    @raise_for_view_error
    def create_session(self, document_id, expires_at=None, is_downloadable=None):
        """
        """

        resource = '{}{}'.format(self.url, SESSIONS_RESOURCE)
        headers = {'Content-type': 'application/json'}
        data = {'document_id': document_id}

        if expires_at:
            data['expires_at'] = expires_at
        if is_downloadable:
            data['is_downloadable'] = True

        data = json.dumps(data)

        response = self.requests.post(resource, headers=headers, data=data)

        return response

    # Convenience Methods

    def ready_to_view(self, document_id):
        """
        """

        document_status = self.get_document_status(document_id)

        return document_status == DONE

    def get_document_status(self, document_id):
        """
        """

        document = self.get_document(document_id).json()

        return document['status']

    @staticmethod
    def create_session_url(session_id, theme=None):
        """
        """
        if not theme:
            theme = 'light'

        return '{}{}/{}{}?theme={}'.format(
            s.VIEW_API_URL,
            SESSIONS_RESOURCE,
            session_id,
            VIEW_RESOURCE,
            theme
        )
