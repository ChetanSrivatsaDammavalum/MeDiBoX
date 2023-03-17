#from ast import literal_eval
from sub_menus import login, registration, caretaker_service, prescription_service
from CustomerCreationService import user_class_test 
from CustomerDatabaseService import read_customerdata_file, upload_customerdata, write_customerdata_dataframe
from PrescriptionDatabaseService import read_prescriptiondata
from PrescriptionCreationService import hourly_prescription, dietbased_prescription

import numpy as np
import itertools

#--------------------------------login menu---------------------------------

def login_menu(df): # customer dataframe passed
    
    print("\n ------------")
    print("< Login Menu >")
    print(" ------------\n")
    print(" Login - 1 \n")
    print(" Registration - 2 \n")
    print(" ------------\n")

    while True:    
        choice = input()
        if choice == '1':
            user_class = login_function(df)
            break
        elif choice == '2':
            user_class = registration_function(df)
            break
        else:
            print(' Wrong input, enter valid option \n')

    return user_class
        
def login_function(df):
    data = {}
    uc = user_class_test
    while True:    
        print("\n- Enter Login Credentials -\n")
        print(" Enter email id: \n")
        email_id = input()
        path = login()
        path.email_id = email_id
        if path.check_email(df):
            print(' Email exists!! \n')
            attempt = 0
            n = 3 # max number of password attempts 
            while attempt < n: 
                print(" Enter password: \n")
                password = input()
                path.password = password
                if path.check_password(df):
                    print(' Password is correct!! ')
                    print(' Loggin in ....! ')
                    data = upload_customerdata( df, 'email_id', email_id)
                    print(' customer data',data)
                    break
                else:
                    attempt+=1
                    print(f' incorrect password !!, try again. Attempts left:{n-attempt} ')
                    if attempt == 3:
                        print(' Failed 3 attempts, cannot login!! ')
            break            
        else:
            print(' incorrect email id, try again! ')
    print('login data dict',data)
    # needs to be optimised!!!
    uc.name = data['name']
    uc.email_id = data['email_id']
    uc.password = data['password']
    uc.gender = data['gender']
    uc.date_of_birth = data['date_of_birth']
    uc.height = data['height']
    uc.weight = data['weight']
    uc.doctor = data['doctor']
    uc.device = data['device']
    #uc.dependents = literal_eval(data['dependents'])
    uc.dependents = data['dependents']
    uc.caregiver = data['caregiver']
    print('dependents type and value in login menu:',uc.dependents,type(uc.dependents))
    # for user: Chetan
    #>>> dependents type and value in login menu: ['Venky', 'Abhinav'] <class 'list'> 

    return uc

def registration_function(df): 
    
    uc = user_class_test

    print("\n- Enter New User Details -\n")
    path = True
    
    print(' Enter user name (no spaces): \n')
    uc.name = input()
    
    while True: 
        print(" Enter email id: \n")
        uc.email_id = input()
        path = registration(uc.email_id).check_email(df)
        if path:
            print(' email id already exists, enter a new id \n')
        else:
             print(' email id is available \n')
             break
        
    print(" Enter password: \n")
    uc.password = input()
    print(' Enter sex: \n')    
    uc.gender = input()
    print(' Enter date of birth (dd.mm.yyy): \n')
    uc.date_of_birth = input()
    print(' Enter height (cm): \n')
    uc.height = input()
    print(' Enter weight (kg): \n')
    uc.weight = input()

    uc.doctor = ''
    uc.device = ''
    uc.dependents = []
    print('dependents type and value in registration menu:',uc.dependents,type(uc.dependents))
    # For new user
    #>>>dependents type and value in registration menu: [] <class 'list'>
    #uc.dependents = np.empty
    uc.caregiver = ''

    return uc

#----------------------------Prescription_service_menu-------------------------

def Prescription_service_menu(uc, pd):
    ps = prescription_service

    while True:
        print("\n ------------------------ ")
        print('< Prescription service menu >')
        print(" ------------------------ \n")
        print(' View prescription - 1 \n')
        print(' Add/modify prescription - 2 \n')
        # print(' View dependent prescription - 3 \n') # need prescription record
        print(' back to main menu - 4')
        print(" ------------------------ \n")

        # needs to me modified!!!!!
        choice = input()
        if choice == '1':
            # view  user prescription
            print(f'printing prescription... \n Prescription Info  of {uc.name}-> \n')
            ps.print_prescription(ps, pd) # !!! NEEDs TO BE CREATED

        elif choice == '2':
            # Add/remove dependent users
            modify_prescription(cs, uc,df)# !!! Need to create 
            
        elif choice == '3':
            print(' need to be updated')
        else:
            break
    return 

# if prescription file exists
def generate_prescription_obj(prescriotion_data):
    neg_col = ['missed_dose_status']
    #print('!!!! filtered prescription data in dictionary form: \n',prescriotion_data )

    prescription_data_obj = []
    for col, data in prescriotion_data.items():            
        if data['prescription_type'] == 'hourly_prescription' :
            prescription_obj =  assign_to_prescription_data_obj(hourly_prescription, data, col)
            prescription_data_obj.append(prescription_obj)
            #print(f'prescription_obj for {col} in generate_prescription_obj: \n', prescription_obj)

        elif data['prescription_type'] == 'dietbased_prescription' :
            prescription_obj =  assign_to_prescription_data_obj(dietbased_prescription, data, col)
            prescription_data_obj.append(prescription_obj)
            #print(f'prescription_obj for {col} in generate_prescription_obj: \n', prescription_obj)

        else: 
            print('\n!!@@!!@@unknown prescription type!!!')

    print( 'prescription data object: \n',prescription_data_obj.__str__(), 'type:\n',type(prescription_data_obj) )
    return prescription_data_obj
        #"""
    #except:
    #    print('No prescription data added')
    #    return None
    

"""
{
'missed_dose_status': {'prescription_type': nan, 'total_qty': nan, 'qty_left': nan, '01:00': 0.0, '01:45': 0.0, '02:00': 0.0, '07:00': 1.0, '10:00': 0.0, '12:45': 0.0, '13:00': 0.0, '16:00': 0.0, '18:30': 1, '18:45': 0.0, '19:00': 0.0, '22:00': 0.0}, 
'paracitamal': {'prescription_type': 'dietbased_prescription', 'total_qty': '20', 'qty_left': '20', '01:00': '0', '01:45': '1', '02:00': '1', '07:00': '0', '10:00': '0', '12:45': '1', '13:00': '0', '16:00': '0', '18:30': '1', '18:45': '1', '19:00': '0', '22:00': '0'}, 
'multivitamin': {'prescription_type': 'dietbased_prescription', 'total_qty': '60', 'qty_left': '60', '01:00': '0', '01:45': '1', '02:00': '1', '07:00': '0', '10:00': '0', '12:45': '1', '13:00': '0', '16:00': '0', '18:30': '1', '18:45': '1', '19:00': '0', '22:00': '0'}, 
'ibuprofin': {'prescription_type': 'hourly_prescription', 'total_qty': '120', 'qty_left': '120', '01:00': '1', '01:45': '0', '02:00': '0', '07:00': '1', '10:00': '1', '12:45': '0', '13:00': '1', '16:00': '1', '18:30': '1', '18:45': '0', '19:00': '1', '22:00': '1'}
}
"""
def assign_to_prescription_data_obj(cls_obj, data, col):
        # displayable items 
        cls_obj.medicine_name = col # columns or main keys in dictionary 
        cls_obj.prescription_type = data['prescription_type'] 
        cls_obj.total_qty = data['total_qty'] # 1: element in medicine column
        cls_obj.qty_left = data['qty_left'] # 2: element in medicine column
        cls_obj.dose_slot = dict(itertools.islice(data.items(), 3 , (len(data)+1)))
        cls_obj.dose_slot = {k: v for k, v in cls_obj.dose_slot.items() if v != '0' and v != np.nan}
        print('dose slot', cls_obj.dose_slot)
        # not displayed
        #print(f'dose_slot for {cls_obj.medicine_name} in assign_to_prescription_data_obj: \n',cls_obj.dose_slot, type(cls_obj.dose_slot))
        #print(f'dose_qty for {cls_obj.medicine_name} in assign_to_prescription_data_obj: \n',cls_obj.dose_slot.values(), type(cls_obj.dose_slot.values()))
        cls_obj.day_qty = sum(int(val) for val in  cls_obj.dose_slot.values()) # used to notify user to refill the medicines
        print('\n daily medicines to take: ', cls_obj.day_qty)
        return cls_obj

# to create new prescription data
def create_new_prescription_obj(data):  
    """!!! needs to to be changed completly !!!"""  
    print("\n New Prescription \n")    
    print(" Enter type of prescription \n")
    print(" Hourly Prescription - 1 \n")
    print(" Dietbased Prescription - 2 \n")    
    while True:    
        choice = input()
        if choice == '1':
            pd = hourly_prescription
            break
        elif choice == '2':
            pd = dietbased_prescription
            break
        else: 
            print(' Enter valid option \n')
            
    print("\n- Enter Prescription Details -\n")
    
    print(' Enter medicine name (no spaces): \n')
    pd.medicine_name = input() 

    if pd.medicine_name in (col for col in data):
        while True:
            print(' medicine already in prescription, do you want to overwrite?(y/n) \n')            
            choice = input()
            if choice == 'n' or choice == 'n':
                return None
            elif choice == 'y' or choice == 'Y':
                print(' Overwriting existing prescription \n')
                break
            else:
                print('invalid responce, try again \n')
            
    print(' Enter quantity of medicine being added: \n')
    pd.total_qty = input()
    pd.qty_left = pd.total_qty
    
    pd.dose_slot = generate_dosage_data(pd)

    return pd

def generate_dosage_data(pd):
    """fucnction to generate dose slots based on prescription types"""

    if pd.prescription_type == 'dietbased_prescription':
        print(' Enter when the medicines are to be taken : (input single option ata time followed be enter) \n')
        pd.dose_when = []
        print('pre_breakfast(0), post_breakfast(1), pre_lunch(2), post_lunch(3), pre_dinner(4), post_dinner(5), Exit(6)')
        while True:
            choice = input()
            if input not in ['0','1','2','3','4','5','6']:
                print(' Enter valid input\n')
            else:
                if choice == '6':
                    break
                else:
                    pd.dose_when.append(choice)
                    
        print(' Generating medicine dosage schedule \n')
        pd.dose_slot = pd.set_dose_slots(pd)
        print('Schedule has been generated: \n',pd.dose_slot)

    elif pd.prescription_type == 'hourly_prescription':
        print(' Enter medicine time between doses: \n')
        pd.dose_period = input() 

        print(' Enter medicine first dosage time: \n')
        pd.dose_start = input() 

        print(' Generating medicine dosage schedule \n')
        pd.dose_slot = pd.set_dose_slots(pd)
        print('Schedule has been generated: \n',pd.dose_slot)

    else: 
        print(' Invalid prescription type \n')
        return None
#----------------------------Caretaker_service_menu-------------------------

def Caretaker_service_menu(uc, df, pd):
    cs = caretaker_service
    while True:
        print("\n ------------------------ ")
        print('< Caretaker service menu >')
        print(" ------------------------ \n")
        print(' View dependents - 1 \n')
        print(' Add/remove dependents - 2 \n')
        print(' View dependent prescription - 3 \n') # need prescription record
        print(' back to main menu - 4')
        print(" ------------------------ \n")

        choice = input()
        if choice == '1':
            # view dependent users
            uc.print_dependents(uc)

        elif choice == '2':
            # Add/remove dependent users
            modify_dependents(cs, uc,df)
         
        elif choice == '3':
            # Add/remove dependent users
            view_dependents_prescription( uc, df, pd)
            
        elif choice == '4':
            print(' need to be updated')
        else:
            break
    return dependents

def modify_dependents(cs, uc,df):
    while True:
        print('\n- Add/remove dependents -\n')
        print(' Add dependent - 1 \n')
        print(' Remove dependent - 2 \n')
        print(' Back - 3 \n')
        choice = input()
        if choice == '1':
            if len(uc.dependents) < 3:
                while True:
                    print(' Enter the name of a dependent to add (no spaces, should be a user): \n')
                    dep = input()
                    if caretaker_service().check_dependents(df, dep):
                        cs.add_dependents(cs, uc, dep)
                        break
                    else: 
                        print(' Entered name is not  user, dependent must be a user \n')
                        print(' cancel retry? (y/n) \n')
                        responce =  input()
                        if responce == 'n' or responce == 'N':
                            break
                        else: 
                            break
            else:
                print(' dependents limit reached')

        elif choice == '2':
            print(' Enter the name of a dependent to remove: \n')
            dep = input()
            cs.remove_dependents(cs, uc, dep)

        else:
            break
def view_dependents_prescription(uc):
    for dependent in uc.dependents:
        get_dependent_prescription(dependent)

def get_dependent_prescription(dependent):
    
    prescription_data_dict = read_prescriptiondata(user_data.email_id)# Type:  dictionary !! chaneg to class object type
    #print('!!!! filtered prescription data in dictionary form: \n',prescription_data_dict )
    prescription_data = generate_prescription_obj(prescription_data_dict)


#---------------------------User_informantion_menu--------------------------

def User_informantion_menu(uc):

    while True:
        print("\n -----------------------")
        print('< User Information Menu >')
        print(" -----------------------\n")
        print(' View user information - 1 \n')
        print(' Add/modify information - 2 \n')
        print(' Change diet timings - 3 \n') # need prescription record
        print(' Back to main menu - 4 \n')
        print(" -----------------------\n")

        choice = input()
        if choice == '1':
            # view user information
            view_user_info(uc) 

        elif choice == '2':
            # modify user information
            modify_information(uc)
            
        elif choice == '3':
            # Change user diet timings !!!!!!!!!!!!
            # change_diet_timings(uc_dict['email_id'])
            print(' need to be updated')
        else:
            break
    
    return 0

def view_user_info(uc):
    return uc.__str__(uc)

def modify_information(uc):
    print('\n- Add/Modify user information -\n')
    print(' choose the field to change \n')
    while True:
        print('\n |------------------------------------------| \n'+
                ' |    Name - 0    |       password - 1      | \n'+
                ' |------------------------------------------| \n'+
                ' |    gender - 2  |    Date of Birth - 3    | \n'+
                ' |------------------------------------------| \n'+
                ' |    height - 4  | weight - 5 | doctor - 6 | \n'+
                ' |------------------------------------------| \n'+
                ' |                 Back - 7                 | \n'+
                ' |------------------------------------------| \n')
        
        choice = input()
        if choice == '0':
            print(' Enter new name \n')
            uc.name = input()
        elif choice == '1':
            print(' Enter new password \n')
            uc.password = input()
        elif choice == '2':
            print(' Enter gender \n')
            uc.gender = input()
        elif choice == '3':
            print(' Enter updated date of birth \n')
            uc.date_of_birth = input()
        elif choice == '4':
            print(' Enter new height \n')
            uc.height = input()
        elif choice == '5':
            print(' Enter new weight \n')
            uc.weight = input()
        elif choice == '6':
            print(' Enter Doctor name \n')
            uc.doctor  = input()
        else:
            break         
#-----------------------------------main_menu-------------------------------

def main_menu(uc,df,pd):
    print(' inside main menu',uc)
    while True:
        print("\n -----------")
        print('< Main Menu >')
        print(" -----------\n")
        print(' Select option \n')
        print(' Prescription service- 1 \n')
        print(' Caretaker service - 2 \n')
        print(' User information - 3 \n')
        print(' Exit Application - 4 \n')


        option = input()

        if option == '1':
            Prescription_service_menu(uc, pd)
        elif option == '2':
            Caretaker_service_menu(uc, df, pd) 
        elif option == '3':
            User_informantion_menu(uc)
        elif option == '4':
            print(' Exiting Application... - 4 \n') 
            break
        else:
            print(' enter valid response')
    return 

#---------------------------------------------------------------------------

def main():
    # get user database
    customer_database = read_customerdata_file()
    customer_database = customer_database.fillna('')
    print(customer_database)

    # Login in page to get specific user info
    user_data = login_menu(customer_database)# Type: class object
    
    # get user prescription info
    prescription_data_dict = read_prescriptiondata(user_data.email_id)# Type:  dictionary !! chaneg to class object type
    #print('!!!! filtered prescription data in dictionary form: \n',prescription_data_dict )
    prescription_data = generate_prescription_obj(prescription_data_dict)
    print('!!!! filtered prescription data as class object: \n',prescription_data )

    # Main menu page to perform user requests and notify when it is time to take medicine
    main_menu(user_data, customer_database, prescription_data)
    
    # update user info and prescriptio information before closing application
    write_customerdata_dataframe(customer_database, user_data)

    exit()


if __name__ == "__main__":
    main()
    
                
