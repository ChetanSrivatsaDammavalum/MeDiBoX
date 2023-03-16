# Create or append data into database of customers
# Retrive data from database of customers
import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from PrescriptionCreationService import hourly_prescription
from PrescriptionCreationService import dietbased_prescription

# check if database exists.
# add data - rows or columns to database
# retrieve data from database

file_loc = os.getcwd() + '/PrescriptionDatabase.csv'
medicine_file_loc = os.getcwd() + '/MedicineDatabase.csv'

#"""
def write_priscriptiondata(prescription_data) -> None:
    print('file_loc',file_loc)
    print('prescription data', prescription_data)
    df = pd.DataFrame(data = prescription_data)
    print( ' Checking database ')

    print('time periods test')
    intervals = pd.timedelta_range(0, freq="15T")
    print(intervals)
    
    try:
        if os.path.exists(file_loc):
            print( ' Database exists ')
            # Check if medicine already exists - email_id
            df_file = pd.read_csv(file_loc)
            if prescription_data['medicine_name'] in df_file.values :               
                print( ' User already exists ')
            else: 
                # code excerpt to write user data
                df.to_csv(file_loc, mode='a', index=False, header=False)
                print( ' User has been added ')
    except:
        # return exception and create new database
        print( ' Database does not exist \n Creating new database')
        df.to_csv(file_loc, index=False, header=True)
        print( ' User has been added ')    
    
#"""

def set_dose_slots_hp(dose_start, dose_period):
        # retun a string of times and doses
        # logic as follows. needs to be rewritten to work in code logic
        dose_slot = []
        dose_start_datetime = datetime.strptime(dose_start,'%H:%M')

        dose_time = dose_start_datetime
        print("hourly dose start time: ",dose_start_datetime," (or) ",dose_time )
        
        dose_time_tmp = str(dose_time)

        dose_slot.append(dose_time_tmp[-8:-3])
                
        time_limit = datetime.strptime("23:59",'%H:%M')
        print(time_limit)

        while(dose_time < time_limit):
            dose_time =  dose_time + timedelta(minutes = int(dose_period))
            dose_time_tmp = str(dose_time)
            dose_time_tmp = dose_time_tmp[-8:-3]
            dose_slot.append(dose_time_tmp)
            print(dose_time)
        return dose_slot

        """
        hourly dose start time:  1900-01-01 09:00:00  (or)  1900-01-01 09:00:00
        1900-01-01 23:59:00
        """

def set_dose_slots_dp(dose_when):
        dose_slot = []
        print("dose times based on diet: \n", dose_when )

        breakfast_time = "09:00"
        breakfast_datetime = datetime.strptime(breakfast_time,'%H:%M')
    
        lunch_time = "13:00"
        lunch_datetime = datetime.strptime(lunch_time,'%H:%M')
    
        dinner_time = "19:00"
        dinner_datetime = datetime.strptime(dinner_time,'%H:%M')
    
        
        # return a string of times and values
        # logic as follows. needs to be rewritten to work in code logic
        for slot in dose_when:
            if slot == "pre_breakfast":
                dose_time =  breakfast_datetime + timedelta(minutes = -15)
            elif slot == "post_breakfast":
                dose_time =  breakfast_datetime + timedelta(minutes = 75)
            elif slot == "post_lunch":
                dose_time =  lunch_datetime + timedelta(minutes = -15)
            elif slot == "post_lunch":
                dose_time =  lunch_datetime + timedelta(minutes = 75)
            elif slot == "post_dinner":
                dose_time =  dinner_datetime + timedelta(minutes = -15)
            else: 
                dose_time =  dinner_datetime + timedelta(minutes = 75)
            dose_time = str(dose_time)
            dose_time = dose_time[-8:-3]
            print(dose_time)

            dose_slot.append(dose_time)

        return dose_slot




def main() -> None:
    # !!!user info!!!!
    # associate each name field to a button click and also check dataframe for repeats in email and unique id
    #user_name = input()
    #email_id = input()
    #password = input()
    #gender = input()
    #date_of_birth = input()
    #height = input()
    #weight = input()

    #--------------------------Prescription------------------------
    # for hourly prescription
    hourly_medicine_name = "asprin"
    hourly_total_qty = 20
    hourly_dose_period = '120' 
    hourly_dose_start = '06:00'
    hourly_dose_qty = '4'
    
    hp = hourly_prescription(hourly_medicine_name, hourly_total_qty, hourly_dose_period, hourly_dose_start, hourly_dose_qty )
    
    #print(hp)

    # for dietbased prescription
    dietbased_medicine_name = "asprin"
    dietbased_total_qty = 20
    dietbased_dose_when = [ 'pre_breakfast', 'post_breakfast', 'pre_lunch', 'post_lunch', 'pre_dinner', 'post_dinner' ]
    dietbased_dose_qty = '2'

    dp = dietbased_prescription(dietbased_medicine_name, dietbased_total_qty, dietbased_dose_when, dietbased_dose_qty )
    #--------------------------------------------------------------

    #------------------------------DATA FRAME----------------------
    user_email = 'ABCD@gmail.com'
    
    # create index col for dataframe
    time_index = []
    intervals = pd.timedelta_range(0, periods= 96,  freq="15T")
    for interval in intervals:
        interval = str(interval)
        interval = interval[-8:-3]
        time_index.append(interval)
   
    # Creating dataframe -> read user_email from customer_Database, 
    prescription_df = pd.DataFrame( [user_email for x in range(len(time_index))],
                          index=time_index,
                          columns=['user_email'])
    
  
    # column insertion method 1
    prescription_df.insert(1, "ibuprofin", {'00:30': '1', '11:00': '1',
           '22:00': '2', '23:30': '1'}, True)
    
    # column insertion method 2
    multivitamin = {'00:30': '1', '11:00': '1',
           '22:00': '2', '23:30': '1'}

    prescription_df['multivitamin'] = multivitamin

    asprin = {'00:30': '1', '11:00': '1',
           '22:00': '2', '23:30': '1'}

    prescription_df['asprin'] = asprin

    #print(weather_df)
    
    # replace nan value in dataframe with 0s
    prescription_df = prescription_df.fillna(0)
    
    print(prescription_df)

    #--------------------------------------------------------------

#-------------------------Prescription Contd.----------------------
    print(hp.set_dose_slots())
    print(dp.set_dose_slots())
#------------------------------------------------------------------
    
if __name__ == "__main__":
    main()

    