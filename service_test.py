
import time
import base64
import uuid
import pandas as pd
from Docker.addressverification import verifyaddress


def bulktest_from_csv(testfile):
    # Load CSV into pandas DataFrame
    df = pd.read_csv(testfile)
    # print(df)

    results_df = pd.DataFrame(columns=['SmartyID','Address1','Address2','City','State','PostalCode','Country','ProcessResult'])

    for index, row in df.iterrows():
        # if (index % 1000 == 0):
        print(f"Row : {index}")
        
        lookupadress = {
                "input_id" : row["SmartyID"]
                , "street" : row["Address1"]
                , "street2": row["Address2"]
                , "city" : row["City"]
                , "state" : row["State"]
                , "zipcode" : row["PostalCode"]
            }
        
        op = verifyaddress(lookupadress)

        # print (op)

        new_row = pd.DataFrame([{
            'SmartyID' : row["SmartyID"]
            , 'Address1' : row["Address1"]
            , 'Address2' : row["Address2"]
            , 'City' : row["City"]
            , 'State' : row["State"]
            , 'PostalCode' : row["PostalCode"]
            , 'Country' : row["Country"]
            , 'ProcessResult' : op["AddressValid"]
            , 'FailureResultReason' : op["analysis"]["footnotes"] if "analysis" in op else ""
            , 'ExtendedResult' : op
        }])
        
        # print (new_row)

        results_df = pd.concat([results_df, new_row], ignore_index=True)

    results_df.to_csv(testfile, index=False)
    print("Results written to : " + testfile)

if __name__ == '__main__':
    
    # Bulk Test Drom CSV
    # bulktest_from_csv('TestData/US Addresses for Smarty.csv')

    lookupadress = {
        "input_id": "1",
        "street": "810 W Yucca St",
        "street2": "",
        "city": "Somerton",
        "state": "AZ",
        "zipcode": "85350"
    }

    # return 
    print(verifyaddress(lookupadress))


 