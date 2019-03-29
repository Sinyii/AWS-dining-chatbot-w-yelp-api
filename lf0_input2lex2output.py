import json
import time
import random
import boto3
import string

def lambda_handler(event, context):
    # chat
    text = event['text']
    print(event)
    
    print('text = ', text)
    
    client = boto3.client('lex-runtime')
    bot_response = client.post_text(
        botName='DiningConcierge',
        botAlias="$LATEST",
        userId='user',
        inputText=text
        )
    
    reply = bot_response['message']
    print(reply)
    current_time = time.localtime()
    now = time.strftime('%m-%d-%Y %H:%M:%S', current_time)
    
    response = {
        "message": reply,
        "time": now
    }
    
    return {
        "statusCode": 200,
        "headers": {
          "X-Requested-With": '*',
          "Access-Control-Allow-Headers": 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
          "Access-Control-Allow-Origin": '*',
          "Access-Control-Allow-Methods": 'POST, OPTIONS'
        },
        "body": json.dumps(response)
    }
