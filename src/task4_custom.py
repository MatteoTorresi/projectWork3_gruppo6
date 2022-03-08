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
