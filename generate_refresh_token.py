import tekore as tk

client_id = 'f63ef670e01d498bbdb1853dd5fe39a2'
client_secret = '69f66ae8edb44d1385156fe83d182c44'
redirect_uri = 'https://example.com/callback'

conf = (client_id, client_secret, redirect_uri)
file = 'tekore.cfg'

token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
tk.config_to_file(file, conf + (token.refresh_token,))