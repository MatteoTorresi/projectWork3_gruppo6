# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils
import json
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Benvenuto nell'applicazione dei vaccini."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Ciao!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class regionOverallIntentHandler(AbstractRequestHandler):
    """Handler for regionOverall."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("regionOverall")(handler_input)

    def handle(self, handler_input):
        # Take the values in the slots and insert them into a dict
        slots = handler_input.request_envelope.request.intent.slots
        # Extract the values from the dict
        region_name = slots["region_name"].value
        month_string = slots["month_string"].value
        period_year = slots["period_year"].value
        
        # Excute and get results from the lambda function
        url = f"https://u92m5xx1tg.execute-api.eu-central-1.amazonaws.com/dev/coviddoses/task_1?region_name={region_name}&period_year={period_year}&month_string={month_string}"
        
        response = requests.request("GET", url)
        data = json.loads(response.text)
        
        if data == "error, wrong variables":
            speak_output = "Il valore o più valori sono errati."
        else:
            # Get all the data from lambda result
            region_name = (data["region_name"])
            month_string = (data["month_string"])
            period_year = (data["period_year"])
            overall_doses = (data["overall_doses"])
            
            # Output alexa
            speak_output = f"Il numero di dosi ricevute dalla regione {region_name} nel mese di {month_string} dell'anno {period_year}, \
            è di {overall_doses} dosi"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Vuoi fare altro?")
                .response
        )


class timeMaxMinDosesIntentHandler(AbstractRequestHandler):
    """Handler for timeMaxMinDoses."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("timeMaxMinDoses")(handler_input)

    def handle(self, handler_input):
        # Take the values in the slots and insert them into a dict
        slots = handler_input.request_envelope.request.intent.slots
        # Extract the values from the dict
        month_string = slots["month_string"].value
        period_year = slots["period_year"].value
        
        # Excute and get results from the lambda function
        url = f"https://u92m5xx1tg.execute-api.eu-central-1.amazonaws.com/dev/coviddoses/task_2?period_year={period_year}&month_string={month_string}"
        
        response = requests.request("GET", url)
        data = json.loads(response.text)
        
        if data == "error, wrong variables":
            speak_output = "Il valore o più valori sono errati."
        else:
            # Get all the data from lambda result
            region_name_max = (data["region_name_max"])
            region_name_min = (data["region_name_min"])
            max_dose = int(data["max_dose"])
            min_dose = int(data["min_dose"])
            period_year = int(data["period_year"])
            month_string = (data["month_string"])
            
            # Output alexa
            speak_output = f"Il massimo di dosi ricevute nel mese di {month_string} del {period_year} è di {max_dose} dosi \
            nella regione {region_name_max}, il minimo invece è di {min_dose} nella regione {region_name_min}"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Vuoi fare altro?")
                .response
        )


class regionDosesIntentHandler(AbstractRequestHandler):
    """Handler for regionDoses."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("regionDoses")(handler_input)

    def handle(self, handler_input):
        # Take the values in the slots and insert them into a dict
        slots = handler_input.request_envelope.request.intent.slots
        # Extract the values from the dict
        region_name = slots["region_name"].value
        
        # Excute and get results from the lambda function
        url = f"https://u92m5xx1tg.execute-api.eu-central-1.amazonaws.com/dev/coviddoses/task_3?region_name={region_name}"
        
        response = requests.request("GET", url)
        data = json.loads(response.text)
        
        if data == "error, wrong variables":
            speak_output = "Il nome della regione è errato."
        else:
            # Get all the data from lambda result
            region_name = (data["region_name"])
            sum_dose = int(data["sum_dose"])
            count_supply = int(data["count_supply"])
            avg_dose = int(data["avg_dose"])
            
            # Output alexa
            if sum_dose == 0:
                speak_output = "Non sono stati consegnati dosi in questa regione"
            else:
                speak_output = f"La media delle dosi ricevute dalla regione {region_name} è di {avg_dose} dosi"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Vuoi fare altro?")
                .response
        )


class regionMaxMinDosesIntentHandler(AbstractRequestHandler):
    """Handler for regionMaxMinDoses."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("regionMaxMinDoses")(handler_input)

    def handle(self, handler_input):
        # Take the values in the slots and insert them into a dict
        slots = handler_input.request_envelope.request.intent.slots
        # Extract the values from the dict
        region_name = slots["region_name"].value
        
        # Excute and get results from the lambda function
        url = f"https://u92m5xx1tg.execute-api.eu-central-1.amazonaws.com/dev/coviddoses/task_4?region_name={region_name}"
        
        response = requests.request("GET", url)
        data = json.loads(response.text)
        
        if data == "error, wrong variables":
            speak_output = "Il nome della regione è sbagliato."
        else:
            # Get all the data from lambda result
            region_name = (data["region_name"])
            max_dose = int(data["max_dose"])
            min_dose = int(data["min_dose"])
            
            # Output alexa
            speak_output = f"Il massimo di dosi ricevute dalla regione {region_name} è di {max_dose} dosi, il minimo invece è di {min_dose}"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Vuoi fare altro?")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Come posso aiutarti? Puoi chiedere il massimo e il minimo delle dosi ricevute da una regione."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Arrivederci!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Scusa, non ho capito cosa mi vuoi chiedere, puoi ripetere?"
        reprompt = "Scusami, non ho capito cosa mi vuoi chiedere, puoi ripetere?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

# For entirely for debugging
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Hai attivato " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = "Ops, qualcosa è andato storto."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(regionOverallIntentHandler())
sb.add_request_handler(timeMaxMinDosesIntentHandler())
sb.add_request_handler(regionDosesIntentHandler())
sb.add_request_handler(regionMaxMinDosesIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
