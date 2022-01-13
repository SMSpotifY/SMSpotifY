import os
from operator import itemgetter

import tekore as tk

from exceptions.Exceptions import InsufficientPermsException, UnrecognizedServiceException, UnrecognizedRequestException
from services.FaunaService import FaunaService
from services.SpotifyService import SpotifyWrapper, SpotifyService


# TODO: Revamp access control, bake permissions into roles that are listed in a designated spot, with
#  flags for every type of request
# TODO: Then implement access control on users as well, with user-level rules taking priority

# TODO Like songs by admins


class OperatorService:
    def __init__(self, fauna_secret):
        self._setup_spotify()
        self._setup_fauna(fauna_secret)

    def _setup_spotify(self, user='Sara'):
        default_device = 'office_echo'
        if user == 'Z':
            default_device = 'beep'
            conf = (
                os.environ['Z_SPOTIFY_CLIENT_ID'],
                os.environ['Z_CLIENT_SECRET'],
                'https://example.com/callback',
                os.environ['Z_REFRESH_TOKEN']
            )
        else:
            conf = tk.config_from_environment(return_refresh=True)
        token = tk.refresh_user_token(*conf[:2], conf[3])
        spotify_service = SpotifyService(tk.Spotify(token))
        self.spotify = SpotifyWrapper(spotify_service, default_device)

    def _setup_fauna(self, secret):
        self.fauna = FaunaService(secret)

    @staticmethod
    def user_has_perms(request_object):
        user, request_type = itemgetter('user', 'request_type')(request_object)
        if user['role'] == 'admin':
            return True
        else:
            allowed_actions = {
                'end_user': ['queue_track', 'queue_album', 'queue_playlist'],
                'non_user': []
            }
            return request_type in allowed_actions[user['role']]

    # TODO: Create a Request class
    def parse_message(self, message_body, number):
        user = self.fauna.get_user_by_phone_number(number)
        if message_body.startswith('https://open.spotify.com/'):
            split_link = message_body.split('/')
            media_type = split_link[3]
            request_type = f'queue_{media_type}'
            request_service = 'spotify'
            data = split_link[4].split('?')[0]
        else:
            # FAUNA
            fauna_commands = ['whitelist']
            spotify_commands = ['set_device', 'get_devices']
            operator_commands = ['set_location']

            split_msg = message_body.split(' ')
            command = split_msg.pop(0)
            data = ' '.join(split_msg)

            request_type = command

            if command in fauna_commands:
                request_service = 'fauna'
                if command == 'whitelist':
                    args = " ".join(split_msg).split(';')
                    name = args[0]
                    num = args[1]
                    role = args[2]
                    data = {
                        'name': name,
                        'number': num,
                        'role': role
                    }
                    request_type = 'create_user'
            elif command in spotify_commands:
                request_service = 'spotify'
            elif command in operator_commands:
                request_service = 'operator'
            else:
                raise UnrecognizedRequestException('Command not recognised. Please try again')

        return_object = {
            'user': user,
            'request_type': request_type,
            'data': data,
            'request_service': request_service
        }

        return return_object

    def handle(self, message_body, number):
        request = self.parse_message(message_body, number)
        if self.user_has_perms(request):
            services = {
                'spotify': self.spotify.handle,
                'fauna': self.fauna.handle,
                'operator': self.handle_internal
            }

            if request['request_service'] in services:
                return services[request['request_service']](request)
            else:
                raise UnrecognizedServiceException('This service is not recognised. Talk to Sara')

        else:
            raise InsufficientPermsException('You do not have sufficient permissions')

    def handle_internal(self, request):
        functions = {
        }
        if request['request_type'] == 'set_location':
            self._setup_spotify(user=request['data'])
            return f'Location set to {request["data"]}'
        if request['request_type'] in functions:
            return functions[request['request_type']](request['data'])
        else:
            raise UnrecognizedRequestException('Unrecognised internal command')
