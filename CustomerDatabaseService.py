# Create or append data into database of customers
# Retrive data from database of customers
import os
import numpy as np
import pandas as pd
import logging
from ast import literal_eval
logging.basicConfig(level = logging.INFO)

# customer database file location
file_loc = os.getcwd() + '/CustomerDatabase.csv'


#--------------------------------------------------------------------------------------------
#                       Read fuctions
#--------------------------------------------------------------------------------------------
def read_customerdata_file():
    """Read csv file and retrieve data as dataframe object"""
    
    if os.path.exists(file_loc): # check if file exists 
        logging.info(' customer database exists ')
        return pd.read_csv(file_loc)
    else: # return exception and empty dataframe
        logging.info(' customer database does not exist ')
        return None

def customerdata_to_record(dataframe):
    """converts specific dataframe row to dictionary type"""

    return dataframe.to_dict('records')[0]

def check_customerdata_from_file(df,search_key, search_value):
    """check specific row values for given key(column)"""

    if search_value in df[search_key].values: 
        logging.info(f' {search_key} exists in database ')
        return True
    else:
        logging.info(f' {search_key} does not exist in database')
        return False

def check_specific_customerdata_from_file(df, row_key, row_value, search_key, search_value):
    """check specific col values for given row loc"""

    if check_customerdata_from_file(df,row_key, row_value):
        location =  df[df[row_key] == row_value].index.to_numpy()
        if df.iloc[location.item()][search_key] == search_value:
            logging.info(f' {search_key} exists in database ')
            return True
        else:
            logging.info(f' {search_key} does notexists in database ')
            return False
    else:
        return False

def read_customerdata(df, search_key, search_value):
    """retrive specific dataframe row in dictionary record form"""

    if check_customerdata_from_file(df,search_key, search_value):
        df_user = df.loc[df[search_key] == search_value]
        return customerdata_to_record(df_user) # return dataframe row as dictionary 
    else:
        return None

def upload_customerdata(df, search_key, search_value):

    user_data_dict = read_customerdata(df, search_key, search_value)
    print('before liteeral_eval',user_data_dict)
    #user_data_dict['dependents'] = literal_eval(user_data_dict['dependents'])
    user_data_dict[search_key] = literal_eval(user_data_dict[search_key])
    #user_data_dict['dependents'] = user_data_dict['dependents'].strip('"]["').split(', ')

    print('after liteeral_eval',user_data_dict)
    
    return user_data_dict

#--------------------------------------------------------------------------------------------
#                       Write fuctions
#--------------------------------------------------------------------------------------------


def write_customerdata_dataframe(customer_database, customer_data) -> None:
    print(file_loc)
    customer_data_dict = customer_data.create_dict(customer_data)
    print(customer_data_dict)
    customer_data_dict['dependents'] = str(customer_data_dict['dependents']) 
    
    logging.info(' Checking for customer database ')
    if os.path.exists(file_loc):
        logging.info(' customer database exists ')
        # Check if user already exists - email_id
        if customer_data_dict['email_id'] in customer_database.values :               
            logging.info( ' User already exists ')
            print('User already exists, Modify data(y/n):')
            choice = input()
            if choice == 'y' or choice == 'Y':
                row_loc = customer_database[customer_database['email_id'] == customer_data_dict['email_id']].index
                #customer_database.loc[row_loc] = customer_data_dict
                for key in customer_data_dict.keys():
                    customer_database.loc[row_loc, key] = customer_data_dict.get(key)
                # print('updated database \n',customer_database)
                customer_database.to_csv(file_loc, mode='w', index=False, header=True)

            else: 
                print('no changes made')
        else: 
            # code excerpt to write user data
            # convert each dict entry to a list
            for keys in customer_data_dict:
                customer_data_dict[keys] = [customer_data_dict[keys]]
            df = pd.DataFrame({ key:pd.Series(value) for key, value in customer_data_dict.items() })
            df.to_csv(file_loc, mode='a', index=False, header=False)
            logging.info( ' User has been added ')
    else:
        # return exception and create new database
        logging.info( ' customer database does not exist \n Creating new customer database')
        df = pd.DataFrame({ key:pd.Series(value) for key, value in customer_data_dict.items() })
        df.to_csv(file_loc, index=False, header=True)
        logging.info( ' User has been added ')

        