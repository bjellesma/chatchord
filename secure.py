import jwt 
from settings import JWT_SECRET

class UserTokens:

    @classmethod
    def create_token(self, username, room, anonymous=True):
        """
        create json web token with username and room for rooms

        Params:
            username {string} - chosen name of user
            room {string} - chosen room of user
            anonymous - True if the user is not authenticated. False if they have authenticated. Default: True

        Returns
            token {string} - string representing payload on server side
        """
        encoded_jwt = jwt.encode(
            {
                'username': username,
                'room': room,
                'anonymous': anonymous
            }, 
            JWT_SECRET,
            algorithm='HS256'
        )
        return encoded_jwt.decode('utf-8')

    @classmethod 
    def read_token(self, encoded_jwt):
        """
        read json web token string and return decoded payload
        """
        decoded_jwt = jwt.decode(encoded_jwt, JWT_SECRET, algorithms=['HS256'])
        return decoded_jwt