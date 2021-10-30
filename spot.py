import requests
import base64
import datetime
import time
import random
import string
import webbrowser
from threading import Thread
from mysecrets import client_id, client_secret

class Spotify:

    def __init__(
    self,
    authorization = False,
    access_token = None,
    refresh_token = None,
    expiration = None
    ):

        # Basic authentication for non-user requests
        self.id = client_id
        self.secret = client_secret
        self.password = base64.b64encode((client_id + ":" + client_secret).encode('ascii'))

        self.access_token = access_token
        self.refresh_token = refresh_token

        self.authorized = authorization if authorization is True else False

        if isinstance(expiration, datetime.datetime):
            if expiration > datetime.datetime.now():
                self.expiration = expiration
            else:
                self.expiration = None
        else:
            self.expiration = None

        # Sanity check
        Check1 = (self.expiration is None)
        Check2 = (self.access_token is None)
        Check3 = (self.refresh_token is None)
        if Check1 or Check2 or Check3:
            self.authorized = False

        # Thread in charge of API requests and maintaining token validity
        self.caller = Thread(target=self._caller, args=(), daemon=True)
        self.caller.start()

    # Mission statement: _caller
    #=========================================================
    # -> Wake up. Are we authorized yet?
    #   -> Compare current time against expiration endlessly
    #       -> Near expiration
    #           -> Refresh
    #       -> Too soon
    #           -> Is there a request to be made?
    #       -> Expired
    #           -> Man, you really must've screwed the pooch.
    #==========================================================
    def _caller(self):
        # Init: verify authorization, obtain if needed
        if self.authorized is False:

            state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            data = {
            "client_id": self.id,
            "response_type": "code",
            "redirect_uri": "https://localhost:5000/callback",
            "scope" : "user-library-read",
            "show_dialog": "true"
            }
            response = requests.get("https://accounts.spotify.com/authorize", params=data)
            print(response.status_code)
            if response.status_code >= 400:
                print(response.reason)
                print(response.request.url)
                print(response.request.body)
            else:
                webbrowser.open(response.url, new=2)

        while True:
            if self.expiration is None:
                return print("Expiration is None.\nTerminating thread.")
            now = datetime.datetime.now()
            if now > self.expiration:
                pass

if __name__ == "__main__":
    # Module isn't meant to be run individually. Debug code.
    client = Spotify()
    time.sleep(2)
