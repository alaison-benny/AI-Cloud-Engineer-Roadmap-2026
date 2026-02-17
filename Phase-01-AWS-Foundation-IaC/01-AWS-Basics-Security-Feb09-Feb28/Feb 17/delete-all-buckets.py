import boto3
import logging

# Configure logging to see progress
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def delete_all_buckets():
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')

    try:
        # 1. Get all buckets
        buckets = list(s3_resource.buckets.all())
        
        if not buckets:
            logging.info("No buckets found in this account.")
            return

        print(f"Found {len(buckets)} buckets. Starting deletion...")

        for bucket in buckets:
            logging.info(f"Processing bucket: {bucket.name}")
            
            # 2. Delete all object versions (Handles versioned & non-versioned buckets)
            # This is more robust than just deleting 'objects'
            bucket.object_versions.all().delete()
            
            # 3. Delete the bucket itself
            bucket.delete()
            logging.info(f"Successfully deleted bucket: {bucket.name}")

        print("\nAll buckets have been removed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Safety Confirmation
    confirm = input("Are you SURE you want to delete ALL S3 buckets? This cannot be undone. (type 'yes' to proceed): ")
    if confirm.lower() == 'yes':
        delete_all_buckets()
    else:
        print("Operation cancelled.")
