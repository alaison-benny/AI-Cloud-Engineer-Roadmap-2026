import logging
import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region='us-east-2'):
    """Create an S3 bucket in a specified region"""

    try:
        s3_client = boto3.client('s3', region_name=region)
        
        # S3 Logic: us-east-1 does NOT use a LocationConstraint. 
        # All other regions (including us-east-2) REQUIRE it.
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )
            
    except ClientError as e:
        logging.error(e)
        return False
    return True

# To run the script:
if __name__ == "__main__":
    MY_BUCKET = "alu-new-bc-created-by-scrpt-2026"
    success = create_bucket(MY_BUCKET)
    if success:
        print(f"Successfully created: {MY_BUCKET}")
