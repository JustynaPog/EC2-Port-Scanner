#!/bin/bash 


if [ $# -ne 3 ]; then
    echo "Użycie: $0 <region> <port> <running (1 lub 0)>"
    exit 1
fi

REGION=$1
PORT=$2
RUNNING=$3

if [ "$RUNNING" -eq 1 ]; then
  STATUS_FILTER="Name=instance-state-name,Values=running"
else
  STATUS_FILTER="Name=instance-state-name,Values=running,stopped"
fi

declare -A arr

SG_IDS=$(aws ec2 describe-security-groups \
  --region "$REGION" \
  --filters Name=ip-permission.to-port,Values="$PORT" \
  --query "SecurityGroups[*].GroupId" \
  --output text)

INSTANCES=$(aws ec2 describe-instances --region "$REGION" \
  --filters $STATUS_FILTER \
  --query "Reservations[*].Instances[*].[InstanceId, SecurityGroups[*].GroupId]" \
  --output text  | paste -sd ' \n')

while read -r LINE; do  
  INSTANCE_ID=$(echo "$LINE" | awk '{print $1}') 
  SG_LIST=$(echo "$LINE" | awk '{$1=""; print $0}' | xargs)

  for I in $SG_IDS; do
    if echo "$SG_LIST"| grep -qw "$I"; then
      arr["$INSTANCE_ID"]+="$I"
    fi
  done  
done <<< "$INSTANCES"	

for key in ${!arr[@]}; do
    echo "instance: ${key} groups: ${arr[${key}]}"
done
