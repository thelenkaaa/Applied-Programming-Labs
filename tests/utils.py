def jwt_authentication_header(token):
    return {'Authorization': f'Bearer {token}'}
