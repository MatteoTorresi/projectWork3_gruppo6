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
