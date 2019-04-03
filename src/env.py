env = {
    'local': {
        'DB_USER': 'zhuzilin',
        'DB_PW': 'zhuzilin',
        'DB_IP': '0.0.0.0',
        'DB_NAME': 'w4111'
    }
}


def get_env(name):
    return env[name]