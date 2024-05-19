import json
import subprocess
import os
import shutil

def lambda_handler(event, context):
    # Define the directory containing your Terraform configuration
    terraform_dir = '/tmp/terraform'
    
    # Create the directory if it doesn't exist
    if not os.path.exists(terraform_dir):
        os.makedirs(terraform_dir)
    
    # Copy the Terraform files to the /tmp directory
    for file in os.listdir('/var/task/terraform'):
        shutil.copy(f'/var/task/terraform/{file}', terraform_dir)
    
    # Change to the Terraform directory
    os.chdir(terraform_dir)

    # Initialize Terraform
    subprocess.check_call(['terraform', 'init'])

    # Apply the Terraform configuration
    subprocess.check_call(['terraform', 'apply', '-auto-approve'])

    # Get the Terraform output
    output = subprocess.check_output(['terraform', 'output', '-json'])
    output_json = json.loads(output)

    return {
        'statusCode': 200,
        'body': json.dumps(output_json)
    }
