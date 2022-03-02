# Project Work PCTO GROUP 6

## Analysis and resolution

The project we worked on asked us to analyze a series of data regarding the distribution of vaccine doses of Covid-19 from the beginning of production up to the last few months in the various Italian regions.

The task has been divided into three main tasks:

1.  in the first task we were asked to input the name of the region in which to carry out the operations, the month and year we wanted to take into consideration for the calculation of the doses sent in total;
2.  the second task required to establish which region had received the maximum and minimum number of doses, given the month and the year of reference;
3.  the third task asked us to make the average of all the doses delivered in a given region, taken as input.

Firstly we analyzed the **structure** of the json file from which had to extract the information on vaccines and their distribution.
The structure of the file is a complex dictionary, containing a list of information for each day and country.  
Each element of the list is divided into several elements:

-   the index of the element within the list,
-   the supplier of the vaccine doses,
-   the number of doses delivered on that date and the date of delivery,
-   the ISTAT code of the region that received the doses,
-   the name of the region.

The json file contains about 6 thousand elements, which increaseas the time to carry out operations, for this reason we have to adopt strategies to optimize the calculation time of each instruction as much as possible becouse a lambda function on amazon server can be excecuted for no more than three seconds.

### TASK 1

#### CODE

```
"""Task 1 project work, Given the region name, month and year calculate the overall number of doses
delivered"""
import json
import os
import re
from datetime import date
import requests


def get_data():
    """Get the data from the request"""
    url = os.getenv('URL')  # Get the URL from the environment variables
    api_response = requests.get(url)  # Get data
    data = api_response.text  # Convert the data to string
    parse_json = json.loads(data)  # Convert the string to a dictionary
    data = parse_json["data"]  # Get the value "data" in the dict

    return data


def check_country(data, region_name):
    """Check if the country name is correct"""
    region_name = region_name.strip().lower()
    # Check if the country name contains a number
    if region_name.isdigit():
        return "error"

    # Check if the country name exist in the list
    for k, info in enumerate(data):
        if info["nome_area"].lower() == region_name:
            return region_name
        # If end of the list
        if k + 1 == len(data):
            print(f"I dati della regione {region_name} non sono presenti nella lista")
            return "error"


def check_year_digits(year):
    """Check if the year is present in the string"""
    match = re.match(r"\d{4}", year)
    if match is not None:
        return match.group()
    return "error"


def check_year(period_year):
    """Check the year"""
    # Return current year if user doesn't input the year
    if period_year == "":
        return date.today().year
    # Check if the year contains a letter
    if not period_year.isdigit():
        return "error"
    # Check if the number of digits is correct
    if check_year_digits(period_year) == "error":
        return "error"
    period_year = check_year_digits(period_year)
    return period_year


def check_month(month_string):
    """Check if the month is correct"""
    # Month name list
    months = ["gennaio", "febbraio", "marzo", "aprile", "maggio",
              "giugno", "luglio", "agosto", "settembre", "ottobre",
              "novembre", "dicembre"]

    month_string = month_string.lower()
    # Return current month if user doesn't input the month
    if month_string == "":
        month_string = months[date.today().month - 1]
        return date.today().month, month_string
    # Check if the name of the month is correct
    if month_string.lower() in months:
        # Associate the month to it's number
        period_month = int(months.index(month_string.lower()) + 1)
        return period_month, month_string
    return "error", "error"


def get_vaccines_name(data):
    """Get the names of all the vaccines"""
    vaccine_names = {}
    for i, info in enumerate(data):
        vaccine_names[info["fornitore"]] = 0
    return vaccine_names


def overall_calc(data, region_name, period_year, period_month):
    """calculation of the overall doses"""
    # Initialization
    overall_doses = 0
    vaccine_names = get_vaccines_name(data)
    for i, info in enumerate(data):
        # Get the year and the month of the data if names match
        if region_name.lower() == info["nome_area"].lower():
            year = int(info["data_consegna"].split('-')[0])
            month = int(info["data_consegna"].split('-')[1])
            # Sum if the time is right
            if int(period_year) == year and period_month == month:
                overall_doses += info["numero_dosi"]
                # Add the vaccine number
                if info["fornitore"] in vaccine_names:
                    vaccine_names[info["fornitore"]] += info["numero_dosi"]

    return overall_doses, vaccine_names


def get_overall(region_name, period_year, month_string):
    """Main"""
    # Get the data from the request
    data = get_data()

    # Get the name of the country
    region_name = check_country(data, region_name)
    if region_name == "error":
        return "error"

    # Get the year
    period_year = check_year(period_year)
    if region_name == "error":
        return "error"

    # Get the number of the month and the name
    period_month, month_string = check_month(month_string)
    if period_month == "error":
        return "error"

    # Get the result of the calculation
    overall_doses, vaccine_names = overall_calc(data, region_name, period_year, period_month)

    dict_result = {
        "region_name": region_name,
        "month_string": month_string,
        "period_year": period_year,
        "overall_doses": overall_doses,
        "vaccine_names": {}
    }

    # Insert the vaccines in the dict
    for i in vaccine_names.keys():
        dict_result["vaccine_names"][i] = vaccine_names[i]

    return dict_result


def lambda_handler(event, context):
    """Lambda function"""
    try:
        info = event["queryStringParameters"]
        outdata = get_overall(info["region_name"], info["period_year"], info["month_string"])
        if outdata == "error":
            return {
                'statusCode': 400,
                'body': json.dumps("error, wrong variables")
            }
        return {
            'statusCode': 200,
            'body': json.dumps(outdata)
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps("error, run interrupted")
        }

```

#### RESOLUTION METHOD

For the resolution of the first task we have divided the code into seven functions plus the main one and the lambda function:

-   With the first function “***get_data***” we take the data that we are going to work with and convert them firstly into a string and then convert them into a dictionary, we then use an environment variable for the link to the json file from which we will extract the data;
-   with the “***check_country***” function we check that the name of the region entered on input is correct or that it does not contain numbers; then we go to check that the region exists in the list of the json file and if it's present than it returns the name of the region, otherwise it returns "error";
-   with the “***check_year***” function we check that the year insered is correct by firstly check if the year is not given, in this case it returnes the current year, then by checking if it actually contains digits and lastly if it contains a sequence of four digits by calling the "***function check_year_digits***" that using a regular expression checks and gets the first sequence of four digits, if all of this is not right, then i returns "error";
-   with the “***check_month***” function we check if a valid month is entered on input, then we also check that no numbers have been entered and lastly we convert the month into the corresponding number using a list of saved months names. if the name of the months is wrong it returns "error";
-  with the "***get_vaccines_name***" function we get the names of all the vaccines delivered in the regions, we save those in a dictionary and then return it;
-   With the “***overall_calc***” function we calculate the total doses that have been delivered. Firstly we call the "get_vaccines_name" fucntion and then with a loop we go through the whole json file, and for each element we compare the name of the country in the file with the name of the country took on input. For each correspondence, we check the month and year, and if they correspond to the month and year given on input we add the vaccine doses to the total and we add the number of vaccines type delivered. The function passes the data to work on, the name of the country, the month and the year as attributes;
-   With the “***get_overall***” (main function), we call all the functions mentioned and return the result into a dictionary;
-   The “***lambda_handler***” function returns the results to the client and checks for errors.

### TASK 2

#### CODE

```
"""Task 2 project work, Given the month and year calculate the region that received the highest/lowest
number of doses"""
import json
import os
import re
from datetime import date
import requests


def get_data():
    """Get the data from the request"""
    url = os.getenv('URL')              # Get the URL from the environment variables
    api_response = requests.get(url)    # Get data
    data = api_response.text            # Convert the data to string
    parse_json = json.loads(data)       # Convert the string to a dictionary
    data = parse_json["data"]           # Get the value "data" in the dict

    return data
    
    
def check_year_digits(year):
    """Check if the year is present in the string"""
    match = re.match(r"\d{4}", year)
    if match is not None:
        return match.group()
    return "error"


def check_year(period_year):
    """Check the year"""
    # Return current year if user doesn't input the year
    if period_year == "":
        return date.today().year
    # Check if the year contains a letter
    if not period_year.isdigit():
        return "error"
    # Check if the number of digits is correct
    elif check_year_digits(period_year) == "error":
        return "error"
    else:
        period_year = check_year_digits(period_year)
        return period_year


def check_month(month_string):
    """Check if the month is correct"""
    # Month name list
    months = ["gennaio", "febbraio", "marzo", "aprile", "maggio",
              "giugno", "luglio", "agosto", "settembre", "ottobre",
              "novembre", "dicembre"]
              
    month_string = month_string.lower()
    # Return current month if user doesn't input the month
    if month_string == "":
        month_string = months[date.today().month - 1]
        return date.today().month, month_string
    # Check if the name of the month is correct
    if month_string.lower() in months:
        # Associate the month to it's number
        period_month = int(months.index(month_string.lower()) + 1)
        return period_month, month_string
    return "error", "error"


def max_min_calc_time(data, period_year, period_month):
    """calculation of the maximum and the minimum doses received by the countries"""
    # Initialization
    region_name_max = ""
    region_name_min = ""
    max_dose = 0
    min_dose = 0
    for i, info in enumerate(data):
        year = int(info["data_consegna"].split("-")[0])
        month = int(info["data_consegna"].split("-")[1])
        dose = info["numero_dosi"]

        if (month == period_month) and (int(period_year) == year):
            if min_dose == 0:
                min_dose = dose
            if max_dose == 0:
                max_dose = dose

            if dose > max_dose:
                region_name_max = info["nome_area"]
                max_dose = dose

            if dose < min_dose:
                region_name_min = info["nome_area"]
                min_dose = dose

    return region_name_max, region_name_min, max_dose, min_dose


def get_max_min_time(period_year, month_string):
    """Main"""
    # Get the year
    period_year = check_year(period_year)
    if period_year == "error":
        return "error"
    
    # Get the number of the month and the name
    period_month, month_string = check_month(month_string)
    if period_month == "error":
        return "error"
        
    # Get the data from the request
    data = get_data()

    # Get the result of the calculation
    region_name_max, region_name_min, max_dose, min_dose = max_min_calc_time(data, period_year, period_month)
    
    dict_result = {
        "region_name_max" : region_name_max,
        "region_name_min" : region_name_min,
        "max_dose" : max_dose, 
        "min_dose" : min_dose,
        "period_year" : period_year,
        "month_string" : month_string
    }

    return dict_result


def lambda_handler(event, context):
    try:
        info = event["queryStringParameters"]
        outdata = get_max_min_time(info["period_year"], info["month_string"])
        if outdata == "error":
            return {
            'statusCode': 400,
            'body': json.dumps("error, wrong variables")
            }
        return {
            'statusCode': 200,
            'body': json.dumps(outdata)
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps("error, run interrupted")
        }


```

For the resolution of the second task we have divided the code into five functions plus the main one and the lambda function:

-   "***get_data***" function;
-    “***check_year_digits***”  function;
-   “***check_year***” fucntion;
-   "***check_month***" function;
-   in the “***get_max_min_time***” function we go through a loop that iterates for each element of the json file, for each iteration checks if the number of doses delivered on that day is less or greater than the number of previous doses checked and if it's true we change the value.
-   in the “***get_max_min_time***” (main function), we call all the functions mentioned and return the result into a dictionary;
-   The “***lambda_handler***” function returns the results and checks for errors

### TASK 3

#### CODE

```
"""Task 3 project work, Given a region calculate the average value of delivered doses over the entire dataset"""
import json
import requests
import os


def get_data():
    """Get the data from the request"""
    url = os.getenv('URL')          # Get the URL from the environment variables
    api_response = requests.get(url)    # Get data
    data = api_response.text            # Convert the data to string
    parse_json = json.loads(data)       # Convert the string to a dictionary
    data = parse_json["data"]           # Get the value "data" in the dict

    return data
    
    
def check_region(data, region_name):
    """Check if the country name is correct"""
    region_name = region_name.strip().lower()
    # Check if the country name contains a number
    if region_name.isdigit():
        return "error"
    
    # Check if the country name exist in the list
    for k, info in enumerate(data):
        if info["nome_area"].lower() == region_name:
            return region_name
        # If end of the list
        if k + 1 == len(data):
            print(f"I dati della regione {region_name} non sono presenti nella lista")
            return "error"
            

def sum_calc(data, region_name):
    """Sum of the doses received by the country"""
    sum_dose = 0
    i = 0
    for i, info in enumerate(data):
        if info["nome_area"].lower() == region_name:
            sum_dose += int(info["numero_dosi"])

    return sum_dose, i


def get_avg(region_name):
    """Main"""
    # Get the data from the request
    data = get_data()
    
    # Get the name of the country
    region_name = check_region(data, region_name)
    if region_name == "error":
        return "error"
    
    # Get the result of the calculation
    sum_dose, i = sum_calc(data, region_name)
    
    dict_result = {
        "region_name" : region_name,
        "sum_dose" : sum_dose,
        "count_supply" : i,
        "avg_dose" : sum_dose//i
    }

    return dict_result
    
    
def lambda_handler(event, context):
    try:
        info = event["queryStringParameters"]
        outdata = get_avg(info["region_name"])
        if outdata == "error":
            return {
            'statusCode': 400,
            'body': json.dumps("error, wrong variables")
            }
        return {
            'statusCode': 200,
            'body': json.dumps(outdata)
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps("error, run interrupted")
        }

```

For the resolution of the third task we have divided the code into four functions plus the main one and the lambda function:

-   “***get_data***” function;
-   “***check_month***” function;
-   “***check_country***” function;
-   with the “***sum_calc***” function, with a loop we check if the region is the same as the region taken on input, if true, we add all of the vaccines doses to the total and in the end we return it
-   with the “***get_avg***” (main function), we call all the functions mentioned and return the result into a dictionary;
-   The “***lambda_handler***” function returns the results and checks for errors

### TASK 4

#### CODE

```
"""Task custom 4 project work, Given a region print the highest/lowest number of doses"""
import json
import requests
import os


def get_data():
    """Get the data from the request"""
    url = os.getenv('URL')          # Get the URL from the environment variables
    api_response = requests.get(url)    # Get data
    data = api_response.text            # Convert the data to string
    parse_json = json.loads(data)       # Convert the string to a dictionary
    data = parse_json["data"]           # Get the value "data" in the dict

    return data
    
    
def check_region(data, region_name):
    """Check if the country name is correct"""
    region_name = region_name.strip().lower()
    # Check if the country name contains a number
    if region_name.isdigit():
        return "error"
    
    # Check if the country name exist in the list
    for k, info in enumerate(data):
        if info["nome_area"].lower() == region_name:
            return region_name
        # If end of the list
        if k + 1 == len(data):
            print(f"I dati della regione {region_name} non sono presenti nella lista")
            return "error"
            

def max_min_calc_region(data, region_name):
    """calculation of the maximum and the minimum doses received by the countries"""
    # Initialization
    max_dose = 0
    min_dose = 0
    for i, info in enumerate(data):
        if info["nome_area"].lower() == region_name:
            if min_dose == 0:
                min_dose = info["numero_dosi"]
            if max_dose == 0:
                max_dose = info["numero_dosi"]

            if info["numero_dosi"] > max_dose:
                max_dose = info["numero_dosi"]

            if info["numero_dosi"] < min_dose:
                min_dose = info["numero_dosi"]

    return max_dose, min_dose


def get_max_min_region(region_name):
    """Main"""
    # Get the data from the request
    data = get_data()
    
    # Get the name of the country
    region_name = check_region(data, region_name)

    # Get the result of the calculation
    max_dose, min_dose = max_min_calc_region(data, region_name)
    
    dict_result = {
        "region_name" : region_name,
        "max_dose" : max_dose,
        "min_dose" : min_dose
    }
    return dict_result
    
    
def lambda_handler(event, context):
    try:
        info = event["queryStringParameters"]
        outdata = get_max_min_region(info["region_name"])
        if outdata == "error":
            return {
            'statusCode': 400,
            'body': json.dumps("error, wrong variables")
            }
        return {
            'statusCode': 200,
            'body': json.dumps(outdata)
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps("error, run interrupted")
        }

```

The task 4 is a custom task that we thought it would be useful.
For the resolution of the fourth task we have divided the code into three functions plus the main one and the lambda function:

-   “***get_data***” function;
-   “***check_country***” function;
-   with the “***max_min_calc_region***” function, with a loop we check if the region is the same as the region taken on input, if true, we check the maximum and minimum doses receaved and we return those;
-   with the “***get_max_min_region***” (main function), we call all the functions mentioned and return the result into a dictionary;
-   The “***lambda_handler***” function returns the results and checks for errors.

### ALEXA

After having implemented all the lambda functions, we took care of creating the skills to be called in alexa to be able to correctly execute the various commands.
Simply we call the lambda function of all the tasks and we extract the data from the returned json data.

#### CODE
```
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
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
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
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
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ciao!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
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
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
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
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Arrivederci!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Scusa, non ho capito cosa mi vuoi chiedere, puoi ripetere?"
        reprompt = "Scusami, non ho capito cosa mi vuoi chiedere, puoi ripetere?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Hai attivato " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
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

```

BLABLA
