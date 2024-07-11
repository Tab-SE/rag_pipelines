import boto3
import os

s3_client = boto3.client('s3')

local_directory = '/data/insights'
bucket_name = 'your-s3-bucket-name'
