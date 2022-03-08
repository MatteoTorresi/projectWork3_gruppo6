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
