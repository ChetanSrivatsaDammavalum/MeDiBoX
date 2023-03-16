from CustomerCreationService import user_class , care_giver, dependents
#from CustomerCreationService import care_giver 
from PrescriptionCreationService import prescription_class as pc
from PrescriptionCreationService import hourly_prescription
from PrescriptionCreationService import dietbased_prescription 
import CustomerDatabaseService as cds
import PrescriptionDatabaseService as pds

import os
import logging
logging.basicConfig(level = logging.INFO)


def check_data(check_key,check_value, check_dict):
    # check if required value in dataframe
    if check_dict[check_key] == check_value:
        logging.info( ' correct password ')
        return True
    else:
        logging.info( ' wrong password ')
        return False

def log_in_menu():
    # main login menu 
    # option to login - if new user
    # option to register - if new user 
    print('LOGIN MENU\n')
    print('Existing user? (y/n)')
    
    choice = input()

    if choice == 'y' or choice == 'Y':
        return login()
    elif choice == 'n' or choice == 'N':
        return registration()
    else:
        print('enter valid response')
        return {}, {}, {}

def login():
    # function to login
    # check if email and password are correct
    print('Enter email id:')
    email_id = input()
    print('Enter password:')
    password = input()
    
    uc_dict = cds.read_customerdata('email_id',email_id)
    
    password_check = check_data('password',password, uc_dict)
    if password_check is True:
        print('logged in')
    else:
        print('wrong password \n restart application')
        exit()
    uc_prescription = pds.read_prescriptiondata(uc_dict['email_id'])
    # med_list = pds.
    # return user info dictionary, prescription dictionary, medicine database dictionary
    return uc_dict, uc_prescription, {}

def registration():
    # function to register a new user
    # collect user information and store in database
    print('REGISTRATION MENU\n')
    print('Enter user name (no spaces):')
    user_name = input()
    print('Enter email id:')
    email_id = input()
    print('Enter password (no spaces):')
    password = input()
    print('Enter sex:')    
    gender = input()
    print('Enter date of birth (dd.mm.yyy):')
    date_of_birth = input()
    print('Enter height (cm):')
    height = input()
    print('Enter weight (kg):')
    weight = input()

    uc = user_class(user_name, email_id, password, gender, date_of_birth, height, weight)
    uc_dict =  vars(uc) # converting class attributes to dictionary

    cds.write_customerdata(uc_dict)

    # return user info dictionary, prescription dictionary, medicine database dictionary
    return uc_dict, {}, {}

#================
def show_prescription(user_email) -> None:
    # function to diaplay prescription of user
    prescription = pds.read_prescriptiondata_df(user_email)
    print('Prescription ',prescription) 
    #prescription = {key:val for key, val in prescription.items() if val != '0'}
    if prescription is not None: # !!!!!!!!!!!!!!!!!!!!!!!!! 
        prescription = pds.non_zero_prescription(prescription, user_email)
        print('non zero prescription',prescription)
    return None

def change_prescrption(user_email) -> None:
    # for hourly prescription
    
    while True:
        
        print('Prescription info\n')

        print('Enter medicine name (no spaces):')
        med_name = input()
        print('Enter total medicine quantity:')
        total_med_qty = input()
        print('Enter dosage type - hourly(1)/dietbased(2):')
        dosage_type = input()
        
        if dosage_type == '1':
            print('hourly dosage information')
            print('Enter time between medicine doses(in minutes):')
            med_hourly_gap = input()
            print('Enter medicine dosage start time(in hh:mm):')
            med_hourly_start = input()
            print('Enter medicine quantiuty per dose:')
            med_hourly_dose_qty = input()
            prescription_per_medicine = hourly_prescription(med_name, total_med_qty, med_hourly_gap, med_hourly_start, med_hourly_dose_qty)
            prescription_per_medicine_dict = vars(prescription_per_medicine)
            prescription_per_medicine_dict['dose_slot'] = prescription_per_medicine.set_dose_slots()
            pds.write_priscriptiondata(prescription_per_medicine_dict, user_email)

        elif dosage_type == '2':
            print('Dietbased dosage information')
            print('Enter diet periods at which medicine needs to be taken: \n')
            print('pre_breakfast(0), post_breakfast(1), pre_lunch(2), post_lunch(3), pre_dinner(4), post_dinner(5), exit(6) ')
            med_dietbased_when = []
            while True:
                entry = input()
                if entry in ['0','1','2','3','4','5']:
                    med_dietbased_when.append(entry)
                else:
                    break
            print('Enter medicine quantiuty per dose:')
            med_dietbased_dose_qty = input()
            prescription_per_medicine = dietbased_prescription(med_name, total_med_qty, med_dietbased_when, med_dietbased_dose_qty)
            prescription_per_medicine_dict = vars(prescription_per_medicine)
            prescription_per_medicine_dict['dose_slot'] = prescription_per_medicine.set_dose_slots()
            pds.write_priscriptiondata(prescription_per_medicine_dict, user_email)

        print('Add another medicine(y/n)\n')
        choice = input()
        if choice == 'n' or choice == 'N':
            print('All medicine have been added')
            break
        else:
            continue
        
    return 
    
def Prescription_service_menu(uc_dict, uc_priscription, medicine_list) -> None : 
    # function to view prescription, add/change prescription, change diet timings,
    
    while True:

        print('Prescription service menu \n')
        print('View prescription - 1 \n')
        print('Add/change prescription - 2 \n')
        print('Change diet timings - 3 \n')
        print('back to main menu - 4')
    
        choice = input()
        if choice == '1':
            # view prescription of user
            show_prescription(uc_dict['email_id'])
        elif choice == '2':
            # Add/change prescription of user
            change_prescrption(uc_dict['email_id'])
        elif choice == '3':
            # Change user diet timings !!!!!!!!!!!!
            # change_diet_timings(uc_dict['email_id'])
            print('need to be updated')
        else:
            break

def modify_dependents(cg_dict) -> None:
    while True:
        print('Add dependent - 1')
        print('Remove dependent - 2')
        print('Exit - 3')
        choice = input()
        if choice == '1':
            if len(cg_dict['dependents']) < 3:
                print('Enter the name of a dependent to add:')
                dep = input()
                if dep not in cg_dict['dependents']:
                    cg_dict['dependents'].append(dep)
                    print('current dependents:',cg_dict['dependents'] )
                    cds.write_customerdata_test(cg_dict)

            else: 
                print("dependents limit reached")
            return print('New dependents list is:', cg_dict['dependents'])

        elif choice == '2':
            print('Enter the name of a dependent to remove:')
            dep = input()
            if dep in cg_dict['dependents']:
                cg_dict['dependents'].remove(dep)
                cds.write_customerdata_test(cg_dict)

            else: 
                print("name not in list")
            return print('New dependents list is:', cg_dict['dependents'])
        else:
            break
        


def Caretaker_service_menu(uc):
    # function to add/remove dependents, view dependent information, view dependent prescription!!!!!!!!!
    cg = care_giver(uc['name'], uc['email_id'], uc['password'], uc['gender'], uc['date_of_birth'], uc['height'], uc['weight'], uc['doctor'], uc['device'],[])
    cg_dict = cg.__dict__
    while True:
        
        print('Caretaker service menu \n')
        print('View dependents - 1 \n')
        print('Add/remove dependents - 2 \n')
        print('View dependent prescription - 3 \n')
        print('back to main menu - 4')
    
        choice = input()
        if choice == '1':
            # view dependent users
            print('Dependents are: ', cg_dict['dependents'])
        elif choice == '2':
            # Add/remove dependent users
            modify_dependents(cg_dict)
            
        elif choice == '3':
            # Change user diet timings !!!!!!!!!!!!
            # change_diet_timings(uc_dict['email_id'])
            print('need to be updated')
        else:
            break

    return 0

def User_informantion_menu():
    # fucntion to add/modify user information
    return

def Settings_menu():
    # Set alarm on/off 
    return

def exit_menu():
    print('Exiting application')
    return exit()


def main_menu(uc_dict, uc_priscription, medicine_list):
    # main login menu 

    while True:

        print('Main Menu\n')
        print('Select option')
        print('Prescription service- 1 \n')
        print('Caretaker service - 2 \n')
        print('User information - 3 \n')
        print('Settings - 4 \n') 
        print('Exit - 5 \n') 

        option = input()

        if option == '1':
            return Prescription_service_menu(uc_dict, uc_priscription, medicine_list)
        elif option == '2':
            return Caretaker_service_menu(uc_dict)
        elif option == '3':
            return User_informantion_menu(uc_dict)
        elif option == '4':
            return Settings_menu(uc_dict)
        elif option == '5':
            return exit_menu()
        else:
            print('enter valid response')
            return 0

def main() -> None:

    # Login menu
    uc_dict, uc_priscription, medicine_list = log_in_menu()

    # main menu
    main_menu(uc_dict, uc_priscription, medicine_list)





    #"""
    #--------------------------Customer------------------------
    # !!!user info!!!!
    # associate each name field to a button click and also check dataframe for repeats in email and unique id
    #user_name = input()
    #email_id = input()
    #password = input()
    #gender = input()
    #date_of_birth = input()
    #height = input()
    #weight = input()
    user_name = 'absd'
    email_id = 'absd@absd.com'
    password = 'absd123458'
    gender = 'm'
    date_of_birth = '01.02.03'
    height = '165'
    weight = '75'
    
    # dataframe fields -> name|customer_id|email|password|gender|date_of_birth|Height|Weight
    #customer_data = {'name': [cc.user_name], 'email_id': [cc.email_id], 'password': [cc.password] , 'gender': [cc.gender], 'date_of_birth': [cc.date_of_birth],'height': [cc.height], 'Weight': [cc.weight]}
    
    #--------------------------------------------------------------
    #--------------------------Prescription------------------------

    # paracitamal,asprin, multivitamin, ibuprofin, budomat

    
if __name__ == "__main__":
    main()
