import os
import datetime

from flask import Blueprint, jsonify
from flask_jwt_extended import decode_token
import click
import requests as req

from cs348_api.extensions import db
from cs348_api.models.user import User

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/', methods=['GET'])
def get_users():
    records = db.session.query(User).all()
    return jsonify(records)


@user.cli.command('register')
@click.argument('name', nargs=1)
@click.argument('email', nargs=1)
@click.argument('password', nargs=1)
def register(name, email, password):
    # Search environment variable for api_uri and port
    api_uri = os.environ.get('CS348_API_URI', 'http://localhost')
    api_port = os.environ.get('CS348_API_PORT', '6608')

    uri = f'{api_uri}:{api_port}'

    body = {
        "name": name,
        "email": email,
        "hashed_password": password
    }

    try:
        res = req.post(f'{uri}/register', json = body)
    except req.exceptions.ConnectionError:
        print(f'Could not connect to CS348 API at {uri}, check if flask server is running')
        return
    
    if res.status_code == 200:
        print(f'[{res.status_code}] User, {name} registered successfully')

        user_data_file = f'{os.path.dirname(os.path.realpath(__file__))}/../../../user_data.md'
        try:
            open(user_data_file, 'r').close()
            with open(user_data_file, 'a') as f:
                f.write('|{name}|{email}|{password}|\n'.format(name=name, email=email, password=password))
        except FileNotFoundError:
            with open(user_data_file, 'w') as f:
                f.write('### This file contains user registration information for debugging purposes\n')
                f.write('These information is generated automatically by script and only show testing accounts only\n')
                f.write('|Name|Email|Password|\n')
                f.write('| :---: | :---: | :---: |\n')
                f.write('|{name}|{email}|{password}|\n'.format(name=name, email=email, password=password))

    elif res.status_code == 400 or res.status_code == 404:
        result = res.json()
        print(f'[{res.status_code}] {result["result"]}: {result["message"]}')
    else:
        print(f'Unknown error: {res.status_code}')


@user.cli.command('login')
@click.argument('email', nargs=1)
@click.argument('password', nargs=1)
def login(email, password):
    # Search environment variable for api_uri and port
    api_uri = os.environ.get('CS348_API_URI', 'http://localhost')
    api_port = os.environ.get('CS348_API_PORT', '6608')

    uri = f'{api_uri}:{api_port}'

    body = {
        "email": email,
        "hashed_password": password
    }

    try:
        res = req.post(f'{uri}/login', json = body)
    except req.exceptions.ConnectionError:
        print(f'Could not connect to CS348 API at {uri}, check if flask server is running')
        return
    
    result = res.json()
    if res.status_code == 200:
        exp_time = decode_token(result['access_token'])['exp']
        exp_time = datetime.datetime.fromtimestamp(exp_time)
        exp_time = exp_time.strftime('%Y-%m-%d %H:%M:%S')

        issue_time = decode_token(result['access_token'])['iat']
        issue_time = datetime.datetime.fromtimestamp(issue_time)
        issue_time = issue_time.strftime('%Y-%m-%d %H:%M:%S')

        print(f'{result["result"]}: {result["message"]}')
        print('You can also check the access token in api/tokens.md folder')
        print(f'Access Token (expires {exp_time}):')
        print(f'    {result["access_token"]}')

        user_data_file = f'{os.path.dirname(os.path.realpath(__file__))}/../../../tokens.md'
        try:
            open(user_data_file, 'r').close()
            with open(user_data_file, 'a') as f:
                f.write('|{email}|{issue}|{exp}|{token}|\n'.format(
                    email=email, 
                    issue=issue_time, 
                    exp=exp_time,
                    token=result["access_token"], 
                ))
        except FileNotFoundError:
            with open(user_data_file, 'w') as f:
                f.write('### This file contains user registration information for debugging purposes\n')
                f.write('These information is generated automatically by script and only show testing accounts only\n')
                f.write('|User email|Issue Date|Expiry Date|Access token|\n')
                f.write('| :---: | :---: | :---: | :---: |\n')
                f.write('|{email}|{issue}|{exp}|{token}|\n'.format(
                    email=email, 
                    issue=issue_time, 
                    exp=exp_time,
                    token=result["access_token"], 
                ))

    else:
        print(f'[{res.status_code}] {result["result"]}: {result["message"]}')
        