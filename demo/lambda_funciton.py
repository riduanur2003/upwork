import json
import boto3
import string
import random
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

iam = boto3.client('iam')

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def lambda_handler(event, context):
    try:
        user_name = random_string(10)
        password = random_string(16)+"7@"

        # Create IAM user
        user_response = iam.create_user(UserName=user_name)
        logger.info(f"Created user: {user_response}")

        # Create login profile for the new user
        iam.create_login_profile(
            UserName=user_name,
            Password=password,
            PasswordResetRequired=True
        )

        return {
            'statusCode': 200,
            'UserName': user_name,
            'Password': password
        }
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return {
            'statusCode': 500,
            'error': str(e),
        }
