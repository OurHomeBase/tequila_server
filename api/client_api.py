'''A module to create OAuth client. It helps with integration testing.'''

from flask import Flask
from flask import jsonify

from persistence import oauth_models
from utils import constants

from api import oauth_api

# pylint: disable=invalid-name
oauth = oauth_api.oauth
app = Flask(__name__, template_folder='templates')
# pylint: enable=invalid-name

app.debug = True
app.secret_key = 'secret'
app.config['DEBUG'] = True

@app.route('/api/client/create')
def create_client():
  '''Creates a test client or returns an existing one.'''
  client = oauth_models.Client.findByClientId(constants.CLIENT_ID)
  if not client:
    client = oauth_models.Client(
        client_id=constants.CLIENT_ID,
        client_secret=constants.CLIENT_SECRET,
        p_redirect_uris=' '.join([
            'http://localhost:8080/c/authorized',
            'http://127.0.0.1:8080/c/authorized',
            'http://127.0.1:8080/c/authorized',
            'http://127.1:8080/c/authorized',
            ]),
        p_defaultscopes='email',
        )
    client.put()

  return jsonify(
      client_id=client.client_id,
      client_secret=client.client_secret)
