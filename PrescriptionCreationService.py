# create new prescription
from datetime import datetime, timedelta
import random
import string
from dataclasses import dataclass , field

"""
{
'missed_dose_status': {'prescription_type': nan, 'total_qty': nan, 'qty_left': nan, '01:00': 0.0, '01:45': 0.0, '02:00': 0.0, '07:00': 1.0, '10:00': 0.0, '12:45': 0.0, '13:00': 0.0, '16:00': 0.0, '18:30': 1, '18:45': 0.0, '19:00': 0.0, '22:00': 0.0}, 
'paracitamal': {'prescription_type': 'dietbased_prescription', 'total_qty': '20', 'qty_left': '20', '01:00': '0', '01:45': '1', '02:00': '1', '07:00': '0', '10:00': '0', '12:45': '1', '13:00': '0', '16:00': '0', '18:30': '1', '18:45': '1', '19:00': '0', '22:00': '0'}, 
'multivitamin': {'prescription_type': 'dietbased_prescription', 'total_qty': '60', 'qty_left': '60', '01:00': '0', '01:45': '1', '02:00': '1', '07:00': '0', '10:00': '0', '12:45': '1', '13:00': '0', '16:00': '0', '18:30': '1', '18:45': '1', '19:00': '0', '22:00': '0'}, 
'ibuprselfofin': {'prescription_type': 'hourly_prescription', 'total_qty': '120', 'qty_left': '120', '01:00': '1', '01:45': '0', '02:00': '0', '07:00': '1', '10:00': '1', '12:45': '0', '13:00': '1', '16:00': '1', '18:30': '1', '18:45': '0', '19:00': '1', '22:00': '1'}
}
"""

# class to create the Prescription database
class prescription_class:
    def __init__(self, medicine_name, total_qty, qty_left, prescription_type, day_qty):
        self.medicine_name = medicine_name # columns or main keys in dictionary 
        self.total_qty = total_qty # 1: element in medicine column
        self.qty_left = qty_left # 2: element in medicine column
        self.prescription_type = prescription_type 
        self.day_qty = day_qty
    
    def update_qty_left(self, dose_qty):
        """ update the quantity of medicine left after each succesful dose """
        val = int(self.qty_left)
        val -= dose_qty
        self.qty_left = str(val)
        return None
    
    def refill_prescription(self, add_qty):
        """ update the quantity of medicine after refilling """
        val_total = int(add_qty) + int(self.qty_left)
        self.total_qty = str(val_total)
        self.qty_left = self.total_qty
        return None

class hourly_prescription(prescription_class):
    def __init__(self, medicine_name, total_qty, qty_left, prescription_type, day_qty, dose_period, dose_start, dose_qty):
        super().__init__(medicine_name, total_qty, qty_left, prescription_type, day_qty)
        self.dose_period = dose_period # in minutes
        self.dose_start = dose_start # first dose time of day "HH:MM"
        self.dose_qty = dose_qty # no of tablets per dose    
        self.prescription_type = 'hourly_prescription'
        self.dose_slot = {'prescription_type': prescription_type, 'total_qty': self.total_qty , 'qty_left': self.qty_left }
    
    def set_dose_slots(self):
        # return a list of string of dose times in "HH:MM" format 

        # converting string "HH:MM" to pandas datetime format
        dose_time = datetime.strptime(self.dose_start,'%H:%M')
                
        # appending first dose time to list of dosage times in string of "HH:MM" format 
        dose_time_str = datetime_to_hh_mm(dose_time)

        # disctionary of time:qty pair
        self.dose_slot[dose_time_str] = self.dose_qty
        
        # setting end of day limit 
        time_limit = datetime.strptime('23:59','%H:%M')
        
        while(dose_time < time_limit):
            dose_time =  dose_time + timedelta(minutes = int(self.dose_period))
            dose_time = datetime_to_hh_mm(self.breakfast_datetime + timedelta(minutes = -15))
            
            # converting time from datetime to string and appending into list of strings of dosage times
            dose_time_str = datetime_to_hh_mm(dose_time)

            # disctionary of time:qty pair
            self.dose_slot[dose_time_str] = self.dose_qty 

        #print("Hourly dosage times",self.dose_slot)
        return self.dose_slot
    
    def calc_day_qty(self):
        self.day_qty = len(self.dose_slot)*self.dose_qty
        return self.day_qty
    
    def print_priscription(self):
        print('------------------------------------------------------------------------------------------ \n'+
            f' || Medicine Name: {self.medicine_name}                                                             \n'+
            '------------------------------------------------------------------------------------------ \n'+
            f' || Quantity left : {self.qty_left}    || Daily dose quantity:{self.day_qty}           \n'+
            '------------------------------------------------------------------------------------------ \n'+
            f' || Dosage timings: {self.dose_slot}                                                          \n'+ 
            '------------------------------------------------------------------------------------------ \n')

class dietbased_prescription(prescription_class):
    def __init__(self, medicine_name, total_qty, qty_left, prescription_type, day_qty, dose_when, dose_qty):
        super().__init__(medicine_name, total_qty, qty_left, prescription_type, day_qty )
        self.dose_when = dose_when
        self.dose_qty = dose_qty
        self.prescription_type = 'dietbased_prescription'
        self.dose_slot = {'prescription_type': prescription_type, 'total_qty': self.total_qty , 'qty_left': self.qty_left }
        
        # setting diet times of user
        self.breakfast_time = "09:00"
        self.lunch_time = "13:00"
        self.dinner_time = "19:00"

        self.pre_timedelta = int('-15')
        self.post_timedelta = int('75')    

        """
        # setting pre and post breakfast dosage times
        self.breakfast_datetime = hh_mm_to_datetime(self.breakfast_time)
        self.pre_breakfast = datetime_to_hh_mm(self.breakfast_datetime + timedelta(minutes = -15))
        self.post_breakfast = datetime_to_hh_mm(self.breakfast_datetime + timedelta(minutes = 75))
        
        # setting pre and post lunch dosage times
        self.lunch_datetime = hh_mm_to_datetime(self.lunch_datetime)
        self.pre_lunch = datetime_to_hh_mm(self.lunch_datetime + timedelta(minutes = -15))
        self.post_lunch = datetime_to_hh_mm(self.lunch_datetime + timedelta(minutes = -75))
        
        # setting pre and post dinner dosage times
        self.dinner_datetime = hh_mm_to_datetime(self.dinner_datetime)
        self.pre_dinner = datetime_to_hh_mm(self.dinner_datetime + timedelta(minutes = -15))
        self.post_dinner = datetime_to_hh_mm(self.dinner_datetime + timedelta(minutes = -75))
        #"""

        # setting pre and post breakfast dosage times
        self.pre_breakfast, self.post_breakfast = pre_post_diet_times( self.breakfast_time, self.pre_timedelta, self.post_timedelta)
        
        # setting pre and post lunch dosage times
        self.pre_lunch, self.post_lunch = pre_post_diet_times( self.lunch_time, self.pre_timedelta, self.post_timedelta)
        
        # setting pre and post dinner dosage times
        self.pre_dinner, self.post_dinner = pre_post_diet_times( self.dinner_time, self.pre_timedelta, self.post_timedelta)
        
    def set_dose_slots(self):
        # return a list of string of dose times in "HH:MM" format 
        # 'pre_breakfast(0), post_breakfast(1), pre_lunch(2), post_lunch(3), pre_dinner(4), post_dinner(5)'
        for slot in self.dose_when:
            if slot == '0': #"pre_breakfast"
                dose_time = self.pre_breakfast
            elif slot == '1':
                dose_time = self.post_breakfast
            elif slot == '2':
                dose_time = self.pre_lunch
            elif slot == '3':
                dose_time = self.post_lunch
            elif slot == '4':
                dose_time = self.pre_dinner
            else: 
                dose_time = self.post_dinner
            
            # converting time from datetime to string and appending into list of strings of dosage times
            self.dose_slot[dose_time] = self.dose_qty

        print("\n diet based dosage times:",self.dose_slot)

        return self.dose_slot
     
    def calc_day_qty(self):
        self.day_qty = len(self.dose_slot)*self.dose_qty
        return self.day_qty
    
    def print_priscription(self):
        print('------------------------------------------------------------------------------------------ \n'+
            f' || Medicine Name: {self.medicine_name}                                                             \n'+
            '------------------------------------------------------------------------------------------ \n'+
            f' || Quantity left : {self.qty_left}    || Daily dose quantity:{self.day_qty}           \n'+
            '------------------------------------------------------------------------------------------ \n'+
            f' || Dosage timings: {self.dose_slot}                                                          \n'+ 
            '------------------------------------------------------------------------------------------ \n')
    
def hh_mm_to_datetime(hh_mm_string):
    """ convert "hh:mm" string to datetime type """
    return datetime.strptime(hh_mm_string,'%H:%M')

def datetime_to_hh_mm(dt_type):
    """ convert "hh:mm" string to datetime type """
    return str(dt_type)[-8:-3]

def pre_post_diet_times( diet_time, pre_timedelta, post_timedelta):
        """ setting pre and post diet dosage times """
        
        diet_datetime = hh_mm_to_datetime(diet_time) # str to datetime format
        pre_diet = datetime_to_hh_mm(diet_datetime + timedelta(minutes = pre_timedelta)) # datetime to str format
        post_diet = datetime_to_hh_mm(diet_datetime + timedelta(minutes = post_timedelta)) # datetime to str format
        
        return pre_diet, post_diet
    