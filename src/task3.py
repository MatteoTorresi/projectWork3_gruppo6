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
