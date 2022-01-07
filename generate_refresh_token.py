from json import load
import os
import os
import tekore as tk
from dotenv import load_dotenv

load_dotenv()

client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
redirect_uri = 'https://example.com/callback'

conf = (client_id, client_secret, redirect_uri)
file = 'tekore.cfg'

token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
tk.config_to_file(file, conf + (token.refresh_token,))