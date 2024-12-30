import boto3
import argparse


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('region', type=str, help='Enter the AWS region')
    parser.add_argument('port', type=int, help='Enter the port to check')
    parser.add_argument('state', type=int, choices=[0, 1], help='Enter instance status (1 for running, 0 for running and stopped)')
    
    args = parser.parse_args()
    return args.region, args.port, args.state

def main():
    region, port, state = get_user_input()

    instance_states = ['running'] if state == 1 else ['running', 'stopped']
    ec2_client = boto3.client('ec2', region_name=region)

    try:
        sg_ids_with_open_port = []
        sg_response = ec2_client.describe_security_groups()
        for sg in sg_response['SecurityGroups']:
            sg_id = sg['GroupId']
            for permission in sg.get('IpPermissions', []):
                if (
                    permission.get('FromPort') == int(port) and
                    permission.get('ToPort') == int(port)
                ):
                    sg_ids_with_open_port.append(sg_id)
                    break  
        instance_response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': instance_states}] 
        )

        for reservation in instance_response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_sgs = [sg['GroupId'] for sg in instance['SecurityGroups']]

                # Check if any attached SG has the open port
                if any(sg_id in sg_ids_with_open_port for sg_id in instance_sgs):
                    print(f"Instance ID: {instance_id}, Security Groups: {', '.join(instance_sgs)}") 
    except Exception as e:
        print(f"Error fetching security groups: {e}")
    
if __name__ == "__main__":
    main()
