env = {
    'local': {
        'DB_USER': 'liufh3',
        'DB_PW': '123456',
        'DB_IP': '0.0.0.0',
        'DB_NAME': 'w4111'
    }
}


def get_env(name):
    return env[name]
