"""
This script gets a Bearer token from unsplash.com in order to like the 
latest photo depending on a search term.

You need to install the `requests` library with the following command:
$ pip install requests

Go to your Unplash app and add 'http://localhost:3000' as a new line in 
the Redirect URI field.

Replace the CLIENT_ID and CLIENT_SECRET constants with the keys from your
own Unplash app.

You can also change SEARCH_QUERY if you prefer.

Press ctrl + c to terminate if the command gets stuck.
"""

import requests
import webbrowser
import http.server as SimpleHTTPServer
import socketserver as SocketServer
from urllib.parse import urlparse, parse_qs
import sys

PORT = 3000


# replace the following constants with the keys from your Unplash app
CLIENT_ID = "replace_with_access_key" # Access Key from your Unplash app
CLIENT_SECRET = "replace_with_secret_key" # Secret Key from your Unplash app

OAUTH_URL = "https://unsplash.com/oauth/authorize"
REDIRECT_URI = f"http://localhost:{PORT}"
SEARCH_QUERY = "wolf"


def like_last_other_photo(params):
    code = params['code'][0]

    TOKEN_URL = "https://unsplash.com/oauth/token"
    TOKEN_PARAMS = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code",
    }

    r =requests.post(TOKEN_URL, params=TOKEN_PARAMS)
    token_info = r.json()

    API_HEADERS = {"Authorization": f"Client-ID {CLIENT_ID}"}

    r = requests.get(
        f'https://api.unsplash.com/search/photos?query={SEARCH_QUERY}&order_by=latest', 
        headers=API_HEADERS
    )

    first_photo = r.json()['results'][0]
    print(f"Likes before {first_photo['likes']}")

    photo_url = first_photo['urls']['regular']
    webbrowser.open(photo_url)

    LIKE_HEADERS = {"Authorization": f"Bearer {token_info['access_token']}"}

    r = requests.post(
        f"https://api.unsplash.com/photos/{first_photo['id']}/like", 
        headers=LIKE_HEADERS
    )

    first_photo = r.json()['photo']
    print(f"Likes after {first_photo['likes']}")
    return photo_url

class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        photo_url = like_last_other_photo(query_components)
        
        self.send_response(302)
        self.send_header('Location', photo_url)
        self.end_headers()
        sys.exit()

Handler = GetHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
authorize_url = OAUTH_URL + f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=public+read_user+read_photos+write_photos+write_likes+write_followers+read_collections+write_collections"
webbrowser.open(authorize_url)

httpd.serve_forever()