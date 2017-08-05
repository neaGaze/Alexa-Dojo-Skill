"""
This code sample is a part of a simple demo to show beginners how to create a skill (app) for the Amazon Echo using AWS Lambda and the Alexa Skills Kit.

For the full code sample visit https://github.com/CodingDojoDallas/Alexa-Dojo-Skill
"""

from __future__ import print_function

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """ Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    SKILL_INFO = {
        'name': "Simple Compliment",
        'invocation': "simple compliment",
    }

    if event['session']['new']:
        on_session_started(
            {'requestId': event['request']['requestId']},
            event['session']
        )

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'], SKILL_INFO)
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], SKILL_INFO)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'], SKILL_INFO)


def on_session_started(request, session):
    """ Called when the session starts """

    info = "on_session_started requestId={} sessionId={}"
    print info.format(request['requestId'], session['sessionId'])


def on_launch(request, session, skill):
    """ Called when the user launches the skill without specifying what they want """

    return get_welcome_response(skill)


def on_intent(request, session, skill):
    """ Called when the user specifies an intent for this skill """

    intent = request['intent']
    intent_name = request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "":
        return get_info_response(skill)
    # elif intent_name == "":
    #     return
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(request, session, skill):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response(skill):
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the {} skill. To get some examples of what this skill can do, ask for help now.".format(skill['name'])
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_info_response(skill):
    session_attributes = {}
    card_title = "{} Info".format(skill['name'])
    speech_output = "{} is an awesome and custom skill.".format(skill['name'])
    reprompt_text = speech_output
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_help_response(skill):
    session_attributes = {}
    card_title = "Help"
    speech_output = "To use the {} skill, try saying... What is {}.".format(skill['name'], skill['invocation'])
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def handle_session_end_request(skill):
    card_title = "{} Ended".format(skill['name'])
    speech_output = "Thank you for using the {} skill!".format(skill['name'])
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
