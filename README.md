# bash_scripts

This script automates the process of identifying AWS EC2 instances and their associated security groups (SGs) that have a specified port open. Below is a step-by-step explanation of how it works:

Input Arguments:

<region>: The AWS region to query (e.g., us-east-1).

<port>: The port to check for open status (e.g., 443 for HTTPS).

<running (1 or 0)>: Specifies whether to include only running instances (1) or both running and stopped instances (0).

Example Output:

For the following input:

./script.sh us-east-1 443 1

The output might look like:

instance: i-0abcd12345 groups: sg-0a1b2c3d sg-0e4f5g6h
instance: i-1bcde23456 groups: sg-0a1b2c3d

This means the specified port (443) is open for the listed instances and their security groups.

Key Notes:

Dependencies: The script requires the AWS CLI to be installed and configured with appropriate permissions.
