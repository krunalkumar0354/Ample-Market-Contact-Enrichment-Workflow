import os
import json
import requests
from hubspot import HubSpot

def main(event):
  # Fetch Amplemarket API key from environment variables
  amplemarket_api_key = os.getenv('Amplemarket')

  # Extract email from the event data
  email = event.get('inputFields').get('email')

  if not amplemarket_api_key:
    print("Amplemarket API key is missing.")
    return

  if not email:
    print("Email is missing from the input fields.")
    return

  url = "https://api.amplemarket.com/people/find"
  querystring = {"email": email}
  headers = {"Authorization": f"Bearer {amplemarket_api_key}"}

  response = requests.get(url, headers=headers, params=querystring)
  # Check for successful response
  if response.status_code == 200:
    person_data = response.json()
    # Set output fields for HubSpot custom coded action
    return{
      "outputFields" : {
      'name': person_data.get('name'),
      'first_name': person_data.get('first_name'),
      'last_name': person_data.get('last_name'),
      'linkedin_url': person_data.get('linkedin_url'),
      'title': person_data.get('title'),
      'headline': person_data.get('headline'),
      'about': person_data.get('about'),
      'current_position_start_date': person_data.get('current_position_start_date'),
      'current_position_description': person_data.get('current_position_description'),
      'image_url': person_data.get('image_url'),
      'location': person_data.get('location'),
      'person_city': list((person_data.get('location')).split(','))[0],
      'person_state': list((person_data.get('location')).split(','))[1],
      'person_country': list((person_data.get('location')).split(','))[2],
      'company_name': person_data.get('company', {}).get('name'),
      'company_website': person_data.get('company', {}).get('website'),
      'company_linkedin_url': person_data.get('company', {}).get('linkedin_url'),
      'company_industry': person_data.get('company', {}).get('industry'),
      'company_size': person_data.get('company', {}).get('size'),
      'company_location': person_data.get('company', {}).get('location'),
      'company_city': list((person_data.get('company', {}).get('location')).split(','))[0],
      'company_state': list((person_data.get('company', {}).get('location')).split(','))[1],
      'company_country': list((person_data.get('company', {}).get('location')).split(','))[2],
      'company_overview': person_data.get('company', {}).get('overview'),
      'company_revenue': person_data.get('company', {}).get('estimated_revenue'),
      'company_technologies': ', '.join(person_data.get('company', {}).get('technologies'))
    }
    }
  else:
    print(f"Error: {response.status_code}, {response.json()}")