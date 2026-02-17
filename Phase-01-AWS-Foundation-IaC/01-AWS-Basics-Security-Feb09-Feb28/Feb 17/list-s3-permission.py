# List all s3 buckets to check pubic and private access list
import boto3
import logging
from botocore.exceptions import ClientError

def check_public_buckets():
    s3_client = boto3.client('s3')
    
    try:
        # എല്ലാ ബക്കറ്റുകളുടെയും ലിസ്റ്റ് എടുക്കുക
        response = s3_client.list_buckets()
        buckets = response['Buckets']
        
        print(f"{'Bucket Name':<50} | {'Status':<10}")
        print("-" * 65)

        for bucket in buckets:
            name = bucket['Name']
            is_public = False
            
            try:
                # 1. Public Access Block കോൺഫിഗറേഷൻ പരിശോധിക്കുക
                # ഇത് 'True' ആണെങ്കിൽ ബക്കറ്റ് സാധാരണഗതിയിൽ പബ്ലിക് ആകില്ല
                pab = s3_client.get_public_access_block(Bucket=name)
                conf = pab['PublicAccessBlockConfiguration']
                
                # എല്ലാ ബ്ലോക്കുകളും എനേബിൾ ആണോ എന്ന് നോക്കുന്നു
                if not all([conf['BlockPublicAcls'], conf['IgnorePublicAcls'], 
                            conf['BlockPublicPolicy'], conf['RestrictPublicBuckets']]):
                    
                    # 2. പോളിസി പബ്ലിക് ആണോ എന്ന് പരിശോധിക്കാനുള്ള ലളിതമായ വഴി
                    # (ഇവിടെ നാം ബക്കറ്റിന്റെ 'Policy Status' നോക്കുന്നു)
                    policy_status = s3_client.get_bucket_policy_status(Bucket=name)
                    if policy_status['PolicyStatus']['IsPublic']:
                        is_public = True
            
            except ClientError as e:
                # ബക്കറ്റിന് പോളിസി ഇല്ലെങ്കിൽ പിശക് വരാം, അത് അവഗണിക്കുക
                if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                    is_public = True # ബ്ലോക്ക് ഇല്ലെങ്കിൽ പബ്ലിക് ആകാൻ സാധ്യതയുണ്ട്

            status = "PUBLIC ⚠️" if is_public else "Private"
            print(f"{name:<50} | {status:<10}")

    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_public_buckets()
