# this is the file which we will use to make the whole python script. 
# note to be taken. boto3 is imported to add AWS SDK to the code

import boto3

def lambda_handler(event, context):
    # Initialize CloudFormation client
    cf_client = boto3.client('cloudformation')

    # Define CloudFormation template parameters
    stack_name = 'MyStack'
    template_body = '''
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "MyS3Bucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "my-unique-bucket-name"
                }
            }
        }
    }
    '''

    # Create or update CloudFormation stack
    try:
        response = cf_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM']  # Add capabilities if needed
        )
        return {
            'statusCode': 200,
            'body': 'CloudFormation stack created successfully'
        }
    except cf_client.exceptions.AlreadyExistsException:
        response = cf_client.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM']  # Add capabilities if needed
        )
        return {
            'statusCode': 200,
            'body': 'CloudFormation stack updated successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
