# സെർവർ സ്റ്റാറ്റസ് ചെക്കപ്പ് Example
# ഒരു EC2 ഇൻസ്റ്റൻസ് ഇപ്പോൾ 'Running' ആണോ എന്ന് പരിശോധിക്കുnna script
import boto3
ec2 = boto3.client('ec2', region_name='us-east-1')
instance_id = 'your-instance-id-here'

response = ec2.describe_instances(InstanceIds=[instance_id])
state = response['Reservations'][0]['Instances'][0]['State']['Name']
print(f"സ്റ്റാറ്റസ്: {state.upper()}")
