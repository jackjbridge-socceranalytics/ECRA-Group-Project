import pandas as pd
import requests
import time

# Script 1
# Script for Geo-Coding
# Made with help from https://www.shanelynn.ie/batch-geocoding-in-python-with-google-geocoding-api/
def google_results(address):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
    geocode_url = geocode_url + "&key={}".format("AIzaSyB8Bxeq8WFN-iB27DEJ2a_qtzrWL3fKfns")

    results = requests.get(geocode_url)

    results = results.json()

    if len(results['results']) != 0:
        answer = results['results'][0]
        output = {
            "formatted_address": answer.get('formatted_address'),
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
            "accuracy": answer.get('geometry').get('location_type'),
            "google_place_id": answer.get("place_id"),
            "type": ",".join(answer.get('types')),
            "postcode": ",".join([x['long_name'] for x in answer.get('address_components')
                                  if 'postal_code' in x.get('types')])
        }
    else:
        output = {
            "formatted_address" : None,
            "latitude": None,
            "longitude": None,
            "accuracy": None,
            "google_place_id": None,
            "type": None,
            "postcode": None
        }
    output['input_string'] = address
    output['number_of_results'] = len(results['results'])
    output['status'] = results.get('status')
    output['response'] = results

    return output

addresses = pd.read_csv('ECRA.csv')
addressCol = addresses['Address'] + addresses['City'] + " " + addresses['State']

results = []
for address in addressCol:
    geocoded = False
    while geocoded is not True:
        geocode_result = google_results(address)
        if geocode_result['status'] == 'OVER_QUERY_LIMIT':
            time.sleep(10 * 60)
            geocoded = False
        else:
            results.append(geocode_result)
            geocoded = True
print("Finished geocoding all addresses")
pd.DataFrame(results).to_csv("newAddress.csv", encoding='utf8')

# Script 2
# Script for combining the data sets so I could get both the school info and geo-coded addresses
addresses = pd.read_csv('ECRA.csv')
usedAddresses = pd.read_csv('address2.csv')
addresses["input_string"] = addresses['Address'] + addresses['City'] + " " + addresses['State']

combinedSet = usedAddresses.merge(addresses, left_on='input_string', right_on='input_string')
print(combinedSet.to_csv("combinedInfo.csv", encoding='utf8'))