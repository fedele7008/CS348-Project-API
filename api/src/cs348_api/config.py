import os 


mysql_config = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'group8'),
    'password': os.environ.get('MYSQL_PASSWORD', 'Password0!'),
    'database': os.environ.get('MYSQL_DATABASE', 'cs348_project')
}


def alchemy_uri():
    return 'mysql://{}:{}@{}/{}'.format(
        mysql_config['user'],
        mysql_config['password'],
        mysql_config['host'],
        mysql_config['database']
    )


def alchemy_debug():
    return 1


def alchemy_development():
    return True


def alchemy_secret_key():
    return 'temporary'


def alchemy_echo():
    return True


def alchemy_track_modifications():
    return False
