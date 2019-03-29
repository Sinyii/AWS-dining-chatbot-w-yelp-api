""" --- Intents --- """
from botocore.vendored import requests
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response
    
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('Dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    print('intent_name = ', intent_name)
    if intent_name == 'GreetingIntent':
        return close(
                output_session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': 'Hello, I am Pops! How can I help you?'
                }
            )
    elif intent_name == 'ThankyouIntent':
        return close(
                output_session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': "You're welcome!"
                }
            )
    elif intent_name == 'DiningSuggestionsIntent':
        # return make_appointment(intent_request)
        location = intent_request['currentIntent']['slots']['location']
        cuisine = intent_request['currentIntent']['slots']['cuisine']
        diningTime = intent_request['currentIntent']['slots']['diningTime']
        numPeople = intent_request['currentIntent']['slots']['numPeople']
        
        yelp_api_key = "YOUR_KEY"
        yelp_search_URL = 'https://api.yelp.com/v3/businesses/search?term={}&location={}&limit=3'.format(cuisine, location)
        
        res = requests.get(yelp_search_URL, headers={"Authorization": "Bearer " + yelp_api_key})

        res_json = res.json()

        if res_json['businesses']:
            response = 'Here are my {} dining suggestions for {} people at {} today:\n '\
            .format(cuisine, numPeople, diningTime)
            for k in range(len(res_json['businesses'])):
                response += str(k+1) + '. ' + res_json['businesses'][k]['name'] + ', located at ' \
                + res_json['businesses'][k]['location']['address1'] + '\n'
                
                if k != len(res_json['businesses']) - 1:
                    response += ', '
            
            response += '.\n Enjoy your meal!'
        else:
            response = "Sorry, I couldn't find {} dining suggestions for {} people at {} today.\n "\
            .format(cuisine, numPeople, diningTime)
        
        return close(
                output_session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': response
                }
            )
        

        # appointment_type = intent_request['currentIntent']['slots']['AppointmentType']
        # date = intent_request['currentIntent']['slots']['Date']
        # appointment_time = intent_request['currentIntent']['slots']['Time']
        # source = intent_request['invocationSource']
        # output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # booking_map = json.loads(try_ex(lambda: output_session_attributes['bookingMap']) or '{}')

    # raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    logger.debug(event)

    return dispatch(event)
