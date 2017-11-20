import json
import boto3
 
dynamodb = boto3.resource('dynamodb', region_name='<aws-region>') 
sms_table = dynamodb.Table('inbound-sms') #The DynamoDB table you will be creating in the AWS console
 
 
def make_response(code, message, detail=None):
    return {
            "statusCode": code,
            "message": message,
            "details": detail
        }
 
 
def update_dynamo(event):
    sms = json.loads(event['body'])
 
    try:
        sms_table.put_item(
            Item=sms
        )
    except Exception as e:
        return make_response(500, 'Dynamo Error: {}'.format(e), detail=sms)
 
    return make_response(200, "SMS saved to Dynamo", detail=sms)
 
 
def receive_inbound_sms(event, context):
    response = update_dynamo(event)
    return response
