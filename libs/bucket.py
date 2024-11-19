import boto3
import os

def load_bucket():
    # instance of boto3 client with AWS credentials
    s3 = boto3.client('s3',
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name = os.environ['AWS_DEFAULT_REGION']
    )

    local_directory = './data/analytics'
    bucket_name = os.environ['AWS_S3_BUCKET']

    # os.walk recursively iterates through files and directories
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            # Construct S3 file path by joining a name with the relative path of each file
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_directory)
            s3_file_path = os.path.join('insights', relative_path)

            try:
                # pushes to S3 and can handle large file sizes
                s3.upload_file(local_file_path, bucket_name, s3_file_path)
                print(f"Uploaded {local_file_path} to {s3_file_path}")
            except Exception as e:
                print(f"Error uploading {local_file_path}: {str(e)}")

    print('Data loaded to s3 bucket successfully!')
