import boto3
import json
import uuid
from datetime import datetime

USERS_TABLE = os.getenv('USERS_TABLE', None)
dynamodb = boto3.resource('dynamodb')
dbTable = dynamodb.Table(USERS_TABLE)

def lambda_handler(event,context):
    route_key = f"{event['httpMethod']} {event['resource']}"
    response_body = {'Message': 'Unsupported route'}
    status_code = 400
    headers = {
        'Content-Type': 'application/json'
        'Access-Control-Allow-Origin': '*'
        }
    try:
        # Get a list of all users
        if route_key == 'GET /users':
            dd_response = ddTable.scan(Select ='ALL_ATTRIBUTES')
            response_body = dd_response['Items']
            status_code = 200
        
        # Get the user details based on the ID

        if route_key == 'GET /users{userid}':
            dd_response = ddTable.get_item(
                Key={'userid': event['pathParameters']['userid']}
            )
            if 'Item' in dd_response:
                response_body = dd_response['Item']
            else:
                response_body = {}
            status_code = 200

        
        # Delete the user based on the ID

        if route_key == 'DELETE /users{usersid}':
            ddTable.delete_item(
                Key={'userid': event['pathParameters'['userid']]}
            )
            response_body = {}
            status_code = 200
        
        #Create a new user
        if route_key == 'POST /users':
            request_json = json.loads(event['body'])
            request_json['timestamp'] = datetime.now().isoformat()
            if 'userid' not in request_json:
                request_json['userid'] = str(uuid.uuid1())

            ddTable.put_item(
                Item=request_json
            )            
            response_body = request_json
            status_code = 200

        #Update the user details based on user id
        if route_key == 'PUT /users/{userid}':
            request_json = json.loads(event['body'])
            request_json['timestamp'] = datetime.now().isoformat()
            request_json['userid'] = event['pathParameters'['userid']]

            ddTable.put_item(
                Item=request_json
            )
            response_body = request_json
            status_code = 200
    except Exception as err:
        status_code = 400
        response_body = {'Error:': str(err)}
        print(str(err))
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body),
        'headers': headers
    }


        