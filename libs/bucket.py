import boto3
import os

def load_bucket(env_vars):
  # instance of boto3 client with AWS credentials
  s3 = boto3.client('s3',
    aws_access_key_id = env_vars['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = env_vars['AWS_SECRET_ACCESS_KEY'],
    region_name = env_vars['AWS_DEFAULT_REGION']
  )

  local_directory = './data/insights'
  bucket_name = 'bragsteinplus'

  # os.walk recursively iterates through files and directories  
  for root, dirs, files in os.walk(local_directory):
      for file in files:
          # Construct S3 file path by joining a name with the relative path of each file
          local_file_path = os.path.join(root, file)
          relative_path = os.path.relpath(local_file_path, local_directory)
          s3_file_path = os.path.join(relative_path)
          
          try:
              # pushes to S3 and can handle large file sizes
              s3.upload_file(local_file_path, bucket_name, s3_file_path)
              print(f"Uploaded {local_file_path} to {s3_file_path}")
          except Exception as e:
              print(f"Error uploading {local_file_path}: {str(e)}")
