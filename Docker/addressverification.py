# -*- coding: utf-8 -*-
import os
import json
from smartystreets_python_sdk import SharedCredentials, StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup
from smartystreets_python_sdk.us_street.match_type import MatchType
from smartystreets_python_sdk.us_zipcode import Lookup as ZIPCodeLookup

auth_id = 'cfcab9d5-ea6a-6d58-7ceb-062a00a07b8b'
auth_token = 'LpClwUO9O75GyVpLVqIz'

def us_zipcode_single_lookup(lookupadress):
    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_zipcode_api_client()

    lookup = ZIPCodeLookup()
    lookup.input_id = lookupadress["input_id"]
    lookup.city = lookupadress["city"] 
    lookup.state = lookupadress["state"] 
    lookup.zipcode = lookupadress["zipcode"] 

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    if not result:
        print("INVALID ZIP CODE")
        return
    else:
        print("VALID ZIP CODE")

        zipcodes = result.zipcodes
        cities = result.cities

        for city in cities:
            print("\nCity: " + city.city)
            print("State: " + city.state)
            print("Mailable City: {}".format(city.mailable_city))

        for zipcode in zipcodes:
            print("\nZIP Code: " + zipcode.zipcode)
            print("Latitude: {}".format(zipcode.latitude))
            print("Longitude: {}".format(zipcode.longitude))

    return

def us_street_single_address(lookupadress):
    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).with_licenses(["us-core-enterprise-cloud"]).build_us_street_api_client()

    lookup = StreetLookup()
    lookup.input_id = lookupadress["input_id"]
    lookup.addressee = ""
    lookup.street = lookupadress["street"]
    lookup.street2 = lookupadress["street2"]
    lookup.secondary = ""
    lookup.urbanization = ""  # Only applies to Puerto Rico addresses
    lookup.city = lookupadress["city"]
    lookup.state = lookupadress["state"]
    lookup.zipcode = lookupadress["zipcode"]
    lookup.candidates = 3
    lookup.match = MatchType.ENHANCED  

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    # print (result)

    candidate_main = {}

    if result:        
        faillist = ['A#', 'B#', 'C#', 'D#', 'F#', 'I#', 'K#', 'V#', 'W#']
        candidate_dict = {'AddressValid': 'True'}
        for candidate in result:
            for key, value in vars(candidate).items():
                # print (key)
                candidate_sub_dict = {}
                if key == 'components':
                    for key, value in vars(value).items():
                        candidate_sub_dict[key] = value
                    candidate_dict['components'] = candidate_sub_dict
                elif key == 'metadata':
                    for key, value in vars(value).items():
                        candidate_sub_dict[key] = value
                    candidate_dict['metadata'] = candidate_sub_dict
                elif key == 'analysis':
                    for key, value in vars(value).items():
                        if key != 'is_ews_match':
                            candidate_sub_dict[key] = value

                        if key == 'footnotes' and value in faillist:
                            candidate_dict['AddressValid'] = 'False'

                    candidate_dict['analysis'] = candidate_sub_dict
                else:
                    candidate_dict[key] = value

            # candidate_main.append(candidate_dict)
            candidate_main = candidate_dict
            break
    else:
        # candidate_dict = {'AddressValid': 'False'}
        # candidate_main.append(candidate_dict)
        candidate_main = {'AddressValid': 'False'}

    return candidate_main


def verifyaddress(lookupadress):

    # lookupadress = {
    #     "input_id": "1",
    #     "street": "810 W Yucca St",
    #     "street2": "",
    #     "city": "Somerton",
    #     "state": "AZ",
    #     "zipcode": "85350",
    # }

    # return 
    # print(us_street_single_address(lookupadress))

    return us_street_single_address(lookupadress)