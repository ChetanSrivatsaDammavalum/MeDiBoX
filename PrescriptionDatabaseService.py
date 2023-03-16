# Create or append data into database of customers
# Retrive data from database of customers
import os
import numpy as np
import pandas as pd
import logging
from threading import Timer, Thread
import itertools # for sliceing dict -> isslice
import time
from PrescriptionCreationService import dietbased_prescription, hourly_prescription
from inputimeout import inputimeout

logging.basicConfig(level = logging.INFO)

# check if database exists.
# add data - rows or columns to database
# retrieve data from database

file_loc = os.getcwd() 
medicine_file_loc = file_loc + '/MedicineDatabase.csv'


#--------------------------------------------------------------------------------------------
#                       Read fuctions
#--------------------------------------------------------------------------------------------

# dictionary output
def read_prescription_file(email_id):
    
    read_file  = file_loc + '/' + email_id +'_PrescriptionDatabase.csv'
    print('file location:',read_file)
    if os.path.exists(read_file):
        return pd.read_csv(read_file)
    else:
        # return exception and empty dataframe
        logging.info( ' User prescription does not exist ')
        return None
    
# dataframe format to dict('tight') and filter out zero dose rows
def read_prescriptiondata(email_id):
        prescription_data_file = read_prescription_file(email_id)
        if prescription_data_file is not None:
            prescription_data = prescription_data_file.to_dict('tight')
            print('non filtered dict: \n',prescription_data)
            return filtered_prescription_data(prescription_data)
        else:
            print(' No prescription file foundb \n')
            return None

# filter out no dosage times from the prescription data and reformat dictionary   
def filtered_prescription_data(df_dict):
    datas = df_dict['data'] 
    datas_filtered = []
    index_times = []
    for data in datas:
        if all(x == '0' for x in data[3:]):
            pass
        else:
            datas_filtered.append(data)
            index_times.append(data[0])
    
    df_dict['data'] = datas_filtered

    print('Index_times :\n',index_times)
    dataframe = pd.DataFrame(data = df_dict['data'], columns= df_dict['columns']).set_index('time')
    #pd.DataFrame(dataframe).set_index('time')
    print('filtered dataframe :\n',dataframe)
    filtered_df_dict = dataframe.to_dict()
    print('filtered_df_dict \n',filtered_df_dict)

    return filtered_df_dict
   
#def write_priscriptiondata(prescription_data, customer_data) -> None:
def write_priscriptiondata(prescription_data, email_id) -> None:
    
    #write_file  = file_loc + '/' + customer_data['email_id'] +'_PrescriptionDatabase.csv'
    write_file  = file_loc + '/' + email_id +'_PrescriptionDatabase.csv'

    print(write_file)
    
    logging.info( ' Checking for medicine database ')    

    # check if medicine database exists
    if os.path.exists(medicine_file_loc):
        logging.info( ' Medicine database exists ')
    
        df_medicine_file = pd.read_csv(medicine_file_loc)
    
        # Check if prescription medicine exists in medicine database
        if prescription_data['medicine_name'] in df_medicine_file.values :               
            logging.info(' Medicine exists in medicine database ')     

        else:
            logging.info(' Medicine not in medicine database ')     

            medicine_df = pd.DataFrame(data = prescription_data['medicine_name'], columns=['medicine_name'], index = [0])
            # append medicine name in the 'medicine name' column of the medicine_database
            medicine_df.to_csv(medicine_file_loc, mode='a', index=False, header=False)
            logging.info( ' medicine has been added to database ')

    else:
        logging.info( ' medicine database does not exist \n Creating new medicine database')
        
        medicine_df = pd.DataFrame(data = prescription_data['medicine_name'], index=[0], columns=['medicine_name'])
        medicine_df.to_csv(medicine_file_loc, index=False, header=True)
        logging.info( ' Medicine has been added to medicine database ')

    logging.info( ' Checking user prescription ')


    time_index = ['Prescription_type', 'total_qty', 'qty_left']
    intervals = pd.timedelta_range(0, periods= 96,  freq="15T")
    for interval in intervals:
        interval = str(interval)
        interval = interval[-8:-3]
        time_index.append(interval)


    #write_file  = file_loc + '/' + customer_data['email_id'] +'_PrescriptionDatabase.csv'
    write_file  = file_loc + '/' + email_id +'_PrescriptionDatabase.csv'

    # checking if prescription database exists before updating or creating prescription data 
    if os.path.exists(write_file):

        logging.info( ' User prescription exists ')
        
        prescription_df = pd.read_csv(write_file)
        
         # Check if medicine already exists in user's prescription
        if prescription_data['medicine_name'] in prescription_df.columns:
            logging.info( ' Medicine already in prescription, updating prescription ')

            # modify the medicine column with new dosage
            # replace column value with new ones 

            logging.info(' Prescription has been updated ')
            pass
        else:
            logging.info(' New medicine in prescription, updating prescription ')

            # adding new medicine to dataframe - new column
            
            prescription_df[prescription_data['medicine_name']] = prescription_df['time'].map(prescription_data['dose_slot'])
            prescription_df.fillna(0, inplace=True)

            #print('prescription dataframe:',df_file)
            prescription_df.head()
            prescription_df.to_csv(write_file, index=False, header=True)

            logging.info( ' Prescription has been updated ')
            
    else:
        logging.info( ' User prescription does not exist \n Creating new prescription')

        # return exception and create new database        
        prescription_df = pd.DataFrame( time_index, index=time_index, columns=['time'])

        prescription_df['diet_times'] = '0'
        
        prescription_df['missed_dose_status'] = '0'

        prescription_df[prescription_data['medicine_name']] = prescription_data['dose_slot']

        prescription_df.fillna(0, inplace=True)
        #prescription_df.to_csv(file_loc, mode='a', index=True, header=True)
    
        prescription_df.to_csv(write_file, index=False, header=True)
        logging.info( ' Prescription has been created and updated ')


"""
Util Functions to perfor data manipulations for the prescription database
"""
#"""
def update_qty_left(df_medicine_dict, dose_qty): # pass in column dict of particular medicine
    
    val = int(df_medicine_dict['qty_left'])
    val -= dose_qty
    return str(val)
#"""

def notification(timeout): # using inputimeout module
    try:
        # Take timed input using inputimeout(prompt,timeout) function
        time_over = inputimeout('\nTime to take your medicine!!\n <Take Dose> - 1 \n <Ignore msg> - 2\n', timeout)
        if time_over == '1':
            print('Medicine has been taken')
            return True
        else:
            print('Missed dose')
            return False

    # Catch the timeout error
    except Exception:
        # Declare the timeout statement
        print('Missed dose')
        return False

# change input from dict to class reference

#def prescription_notification_servive(time_dict, filtered_df_dict):
def prescription_notification_servive(filtered_df_dict):  

    """need to be rewritten to account for datafrae dict changes"""

    print('\n !!!! inside notification thread !!!',filtered_df_dict)
    neg_col = ['missed_dose_status']
    # """
    while True:
        #if time.strftime("%H:%M") in filtered_df_dict['missed_dose_status']:
        if '18:30' in filtered_df_dict['missed_dose_status']:

            #print('Current dosage time: ', time.strftime("%H:%M"))
            print('Current dosage time: ', '18:30')
            
            print('Medicines to take are: \n')
            
            for col in (col for col in filtered_df_dict if col not in neg_col):  # constructor to get medicine cols from filtered_df_dict

                #dose_qty = int(filtered_df_dict[col][time.strftime("%H:%M")])
                dose_qty = int(filtered_df_dict[col]['18:30'])
                
                if dose_qty != 0:
                    print(f'{col}, {dose_qty} table/s ')

            resp = notification(10)
            
            if resp == True:

                for col in (col for col in filtered_df_dict if col not in neg_col):  # constructor to get medicine cols from filtered_df_dict
                    
                    #dose_qty = int(filtered_df_dict[col][time.strftime("%H:%M")])
                    dose_qty = int(filtered_df_dict[col]['18:30'])
                    if dose_qty != 0:
                        filtered_df_dict[col]['qty_left'] = update_qty_left(filtered_df_dict[col], dose_qty)
            else: 
                #filtered_df_dict['missed_dose_status'][time.strftime("%H:%M")] = 1
                filtered_df_dict['missed_dose_status']['18:30'] = 1
                break                        
        else:
            time.sleep(10)    
    
def main():

    email_id = 'Chetan@gmail.com'

    #_________ read test___________
    """ read data frame and convert data suitable for using with prescription creation service class """ 

    filtered_df_dict = read_prescriptiondata(email_id)
    
    print(f'prescription of {email_id} \n')    
    #print('Prescription data info:\n',df.info)

    # removing all times with no prescribed doses 
    
    
    # """ Move to function with in read prescription 

    # """
    
    
    # from filtered_df_dict, for each medicine get prescription type, total qty, qty left, dose times by accessing nested dict
    # eg. for 'paracitamal', prescription_type = filtered_df_dict['paracitamal'][0], total_qty = filtered_df_dict['paracitamal'][1], 
    # qty_left = filtered_df_dict['paracitamal'][2], dose_times = dict(itertools.islice(filtered_df_dict['paracitamal'].items(), 3 ,12)) 
    # map keys of 'time' and 'medicine_name' to display time:dose pairs to user 

    # itertools.islice(iterable, start, stop[, step]), start is included and stop is not
    #time_dict = dict(itertools.islice(filtered_df_dict['time'].items(), 3 , 12))
    #print('Times       : ',time_dict)
    
    #print('paracitamal : ',dict(itertools.islice(filtered_df_dict['paracitamal'].items(), 3 , 12)))
    #print('multivitamin: ',dict(itertools.islice(filtered_df_dict['multivitamin'].items(), 3 , 12)))
    
    
    # dataframe statistical operations

    """"""
    #print('qty_left of multivitanin : ',filtered_df_dict['multivitamin'][2],'\n type:',type(filtered_df_dict['multivitamin'][2]))
    
    #dose_qty = 2
    #filtered_df_dict['multivitamin'][2] = update_qty_left(filtered_df_dict['multivitamin'], dose_qty)
    
    #print('qty_left of multivitanin after update: ',filtered_df_dict['multivitamin'][2], ' type: ',type(filtered_df_dict['multivitamin'][2]))

    #print('updated dataframe: \n',filtered_df_dict)
    """"""

    # try df.query() method
    # set column datatypes

    # =========================================================================================
    """ Time check and notification function """
    # =========================================================================================
    print('paracitamal : ',filtered_df_dict['paracitamal'])
    print('multivitamin: ',filtered_df_dict['multivitamin'])
    
    print('current time is: ', time.strftime("%H:%M"), type(time.strftime("%H:%M")))
    #prescription_notification_servive(time_dict, filtered_df_dict)
    
    prescription_notification_servive(filtered_df_dict)
    
    print('updated data:\n', filtered_df_dict)
  

    """ Threading notification check """
    #"""
    # create a thread for notification service
    thread = Thread(target =prescription_notification_servive, args= filtered_df_dict) # set thread as daemon
    thread.start()

    while True:
        print('\n updated data:\n')
        print('paracitamal : ',filtered_df_dict['paracitamal'])
        print('multivitamin: ',filtered_df_dict['multivitamin'])
        time.sleep(60)

    #"""
        #print('Exit the application? y/n')
        #check = input()
        #if check == 'y' or check == 'Y':
        #        exit()
        #else:
        #    pass
    # """
    # =========================================================================================    
    
    
if __name__ == "__main__":
    main()
    