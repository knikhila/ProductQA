from __future__ import print_function


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
         "amzn1.ask.skill.c03d49a6-26ce-4846-9667-c35c75e0069d"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent_name)

    # Dispatch to your skill's intent handlers
    # TODO: Add cancel intent handling
    if intent_name == "DescriptionIntent":
        return getDescription(intent, session)
    elif intent_name == "AgeIntent":
        return ageToPlaySuperMarioOdyssey(intent, session)
    elif intent_name == "ComparisonIntent":
        return compareProducts(intent, session)
    elif intent_name == "SuperlativeIntent":
        return superlativeProduct(intent, session)
    elif intent_name == "KindBar":
        return kindbarAnswer(intent, session)
    elif intent_name == "SuperMario":
        return superMarioAnswer(intent, session)
    elif intent_name == "EchoDotIntent":
        return echoDotAnswer(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.StopIntent":
        session_attributes = {}
        card_title = "Goodbye"
        speech_output = "Goodbye!"
        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        reprompt_text = None
        should_end_session = True
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Product Advisor!" \
                    #"I have information on four products - " \
                    #"Echo Dot, Echo Show, Kind bars and Super Mario Odyssey Nintendo Switch. " \
                    #"What product would you like to learn about?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what product would you like to learn more about?" \
                    "If you want to hear about all products say all"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getDescription(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_output = "Nothing"

    if 'product' in intent['slots']:
        product = intent['slots']['product']['value']
        session_attributes = create_attribute("product", product)
        if 'feature' in intent['slots']:
            if 'value' in intent['slots']['feature']:
                feature = intent['slots']['feature']['value']
                session_attributes.update(create_attribute("feature", feature))
                speech_output = "Your product is " + \
                        product + " and the feature you requested for is " + \
                        feature
            
        #if 'size' in intent['slots']:
        #    size = intent['slots']['size']['value']
        #    session_attributes = create_attribute("size", size)
        
        reprompt_text = "You can ask me your favorite color by saying, " \
                       "what's my favorite color?"
        #get_information_from_session(session)
   
    else:
        speech_output = "I'm not sure what product you are looking for. " \
                        "Please try again."
        reprompt_text = "I'm not sure what product you are looking for. " \
                        "You can tell me the product by saying."\
                        "I want to know about Echo Dot"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def create_attribute(key, value):
    return {key: value}
    
def ageToPlaySuperMarioOdyssey(intent, session):
    session_attributes = {}
    card_title = "Age to play SuperMarioOdyssey"
    speech_output = "Anyone 10 years or older can play Super Mario Odyssey."
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
            
def kindbarAnswer(intent, session):
    card_title = intent['name']
    product = intent['slots']['product']['value']
    session_attributes = create_attribute("product", product)
    should_end_session = False
    speech_output = "Sorry, I cannot help with that"
    reprompt_text = "Tell me what information you what to know about kind bar"
    
    if 'ingredient' in intent['slots']:
        if 'value' in intent['slots']['ingredient']:
            ingredient = intent['slots']['ingredient']['value']
            session_attributes.update(create_attribute("ingredient", ingredient ))
            speech_output = "Give this info to Satish, product: " + product + " ingredient:  " + ingredient
    if 'nutrition' in intent['slots']:
        if 'value' in intent['slots']['nutrition']:
            nutrition = intent['slots']['nutrition']['value']
            session_attributes.update(create_attribute("nutrition", nutrition ))
            speech_output = "Give this info to Satish, product: " + product + " nutrition:  " + nutrition
    if 'feature' in intent['slots']:
        if 'value' in intent['slots']['feature']:
            feature = intent['slots']['feature']['value']
            session_attributes.update(create_attribute("feature", feature))
            speech_output = "Give this info to Satish, product: " + product + " feature:  " + feature
            if feature == 'calories':
                if 'value' in intent['slots']['nutrition']:
                    nutrition = intent['slots']['nutrition']['value']
                    session_attributes.update(create_attribute("nutrition", nutrition ))
                    speech_output = "Give this info to Satish, product: " + product + " feature:  " + feature + " nutrition " + nutrition
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

def superMarioAnswer(intent, session):
    card_title = intent['name']
    product = intent['slots']['product']['value']
    session_attributes = create_attribute("product", product)
    should_end_session = False
    speech_output = "Sorry, I cannot help with that"
    reprompt_text = "Tell me what information you what to know about super Mario odyssey game"
    if 'gameinfo' in intent['slots']:
        if 'value' in intent['slots']['gameinfo']:
            gameinfo = intent['slots']['gameinfo']['value']
            session_attributes.update(create_attribute("gameinfo", gameinfo ))
            speech_output = "Give this info to Satish, product: " + product + " gameinfo:  " + gameinfo
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

def compareProducts(intent, session):
    card_title = "Compare Products"
    should_end_session = False
    speech_output = ""
    session_attributes = {}
    if 'productOne' in intent['slots']:
        if 'value' in intent['slots']['productOne']:
            product = intent['slots']['productOne']['value']
            session_attributes.update(create_attribute("productOne", product))
            speech_output = "Your productOne is " + product
    if 'productTwo' in intent['slots']:
        if 'value' in intent['slots']['productTwo']:
            product = intent['slots']['productTwo']['value']
            session_attributes.update(create_attribute("productTwo", product))
            speech_output = speech_output + " and your ProductTwo is " + product
    if 'comparison' in intent['slots']:
        comparison = intent['slots']['comparison']['value']
        session_attributes.update(create_attribute("comparison", comparison))
        speech_output = speech_output + " Comparison Is " + comparison
    reprompt_text = "I'm not sure what product you want to compare. " \
                    "You can ask me the products by saying."\
                    "I want to know the difference between Echo Dot and Echo Show"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def superlativeProduct(intent, session):
    card_title = "Superlative Product"
    should_end_session = False
    speech_output = ""
    session_attributes = {}
    if 'productFamily' in intent['slots']:
        if 'value' in intent['slots']['productFamily']:
            product = intent['slots']['productFamily']['value']
            session_attributes.update(create_attribute("productFamily", product))
            speech_output = "Your productFamily is " + product
        
    if 'superlatives' in intent['slots']:
        superlatives = intent['slots']['superlatives']['value']
        session_attributes.update(create_attribute("superlatives", superlatives))
        speech_output = speech_output + " and Comparison Is " + superlatives
        
    reprompt_text = "I'm not sure what product you want to learn about. " \
                    "You can ask me about the products by saying."\
                    "I want to know the cheapest Echo"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def echoDotAnswer(intent, session):
    card_title = intent['name']
    should_end_session = False
    speech_output = ""
    session_attributes = {}
    if 'Facts' in intent['slots']:
        if 'value' in intent['slots']['Facts']:
            Facts = intent['slots']['Facts']['value']
            session_attributes.update(create_attribute("Facts", Facts))
            speech_output = "Your Facts is " + Facts
    if 'product' in intent['slots']:
        if 'value' in intent['slots']['product']:
            product = intent['slots']['product']['value']
            session_attributes.update(create_attribute("product", product))
            speech_output = speech_output + " and your product is " + product
    if 'capability' in intent['slots']:
        if 'value' in intent['slots']['capability']:
            capability = intent['slots']['capability']['value']
            session_attributes.update(create_attribute("capability", capability))
            speech_output = speech_output + " and your capability is " + capability
    if 'question_type' in intent['slots']:
        if 'value' in intent['slots']['question_type']:
            question_type = intent['slots']['question_type']['value']
            session_attributes.update(create_attribute("question_type", question_type))
            speech_output = speech_output + " and your question_type is " + question_type
    if 'usage' in intent['slots']:
        if 'value' in intent['slots']['usage']:
            usage = intent['slots']['usage']['value']
            session_attributes.update(create_attribute("usage", usage))
            speech_output = speech_output + " and your usage is " + usage
    reprompt_text = "I'm not sure what you want to learn about. " \
                    "You can ask me about the products by saying."\
                    "I want to know the how expensive is the Echo Dot"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# To get something from attributes
def get_information_from_session(session):
    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    if "product" in session.get('attributes', {}):
        product = session['attributes']['product']
        speech_output = "Your product is " + product
        if "feature" in session.get('attributes', {}):
            feature = session['attributes']['feature']
            speech_output = speech_output + " and the feature is " + feature
    else:
        speech_output = "I'm not sure what your product is. " 
        should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

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