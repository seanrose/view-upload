from time import sleep
from flask import Flask, request, render_template, jsonify
from boxview import BoxViewClient
from boxviewerror import BoxViewError

app = Flask(__name__)
NO_EXPIRE = 'no_expire'
THE_FUTURE = '4013-12-23T05:21:09.697Z'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/desktop-upload', methods=['POST'])
def desktop_upload_document():
    """
    """
    print str(request.form)
    box_view_client = BoxViewClient()
    uploaded_file = request.files['file']

    try:
        document = box_view_client.multipart_upload_document(uploaded_file)
    except(BoxViewError):
        return jsonify({'error': 'an error occurred'}), 400

    document_id = document.json()['id']
    print 'Document ID is {}'.format(document_id)

    return jsonify(document.json())


@app.route('/url-upload', methods=['POST'])
def url_upload_document():
    """
    """
    box_view_client = BoxViewClient()
    document_url = request.form['document-url']

    try:
        document = box_view_client.upload_document(document_url)
    except(BoxViewError):
        return jsonify({'error': 'an error occurred'}), 400

    document_id = document.json()['id']
    print 'Document ID is {}'.format(document_id)

    return jsonify(document.json())


@app.route('/sessions', methods=['POST'])
def create_session():
    """
    """
    sleep(2)
    box_view_client = BoxViewClient()
    document_id = request.form['document_id']

    should_expire = request.form['expire']
    if should_expire == NO_EXPIRE:
        expires_at = THE_FUTURE
    else:
        expires_at = None

    try:
        api_response = box_view_client.create_session(document_id, expires_at)
    except(BoxViewError):
        return jsonify({'error': 'an error occurred'}), 400

    if api_response.status_code == 202:
        return jsonify({'status': 'much undone'}), 202
    else:
        session = api_response.json()
        session_url = box_view_client.create_session_url(session['id'])
        print 'Session is {}'.format(session_url)

        combined_response = {
            'session_url': session_url,
            'session': session
        }
        return jsonify(combined_response)


@app.route('/webhook', methods=['POST', 'GET'])
def webhook_success():

    print request.data
    return "OK"


def create_session_for_document(document_id,
                                box_view_client,
                                expires_at=None):
    """
    Given a box_view_client and document_id,
    creates a session for that document by polling
    the session endpoint
    """

    # The approximate conversion time for logging purposes
    wait_time = 0
    while True:
        sleep(1)
        wait_time += 1
        try:
            api_response = box_view_client.create_session(document_id,
                                                          expires_at)
            if api_response.status_code == 201:
                session = api_response.json()
                break
        except(BoxViewError):
            return jsonify({'error': 'an error occurred'}), 400

    session_url = box_view_client.create_session_url(session['id'])

    print 'Session is {}'.format(session_url)

    combined_response = {
        'session_url': session_url,
        'session': session
    }
    return combined_response

if __name__ == '__main__':
    app.debug = True
    app.run()
