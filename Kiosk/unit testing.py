import boto3
from boto3.dynamodb.conditions import Key

current_user = '5871857'
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
balance_table = dynamodb.Table('Balance')
table = dynamodb.Table('Order')
resp = balance_table.query(KeyConditionExpression=Key('ID').eq(str(current_user)))
current_balance = (resp.get('Items'))[0].get('Balance')

print(current_balance)