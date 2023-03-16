# create new user and take user data
# check if user is already existing
#from ast import literal_eval
import random
import string

# class to create the customer record
class user_class_test:
    def __init__(self, name, email_id, password, gender, date_of_birth, height, weight, doctor, device, dependents , caregiver ):
 
        self.name = name
        self.email_id = email_id 
        self.password = password
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.height = height
        self.weight = weight
        self.doctor = doctor
        self.device = device
        self.dependents = dependents
        self.caregiver = caregiver
    
    def __str__ (self):
        return print('\n User Info -> \n' +
                     '------------------------------------------------------------------------------------------ \n'
                    f' || Name: {self.name}      || Email id: {self.email_id}          \n'+
                     '------------------------------------------------------------------------------------------ \n'
                    f' || gender: {self.gender}    || Date of Birth:{self.date_of_birth}        \n'+
                     '------------------------------------------------------------------------------------------ \n' +
                    f' || height: {self.height}    || weight: {self.weight}     || doctor:{self.doctor}     \n'+
                     '------------------------------------------------------------------------------------------ \n'
                    f' || dependents: {self.dependents}      \n'+
                     '------------------------------------------------------------------------------------------ \n'
                    f' ||  caregiver: {self.caregiver}      || device: {self.device}         \n' 
                     '------------------------------------------------------------------------------------------ \n')

    def create_dict(self):
        #
        dict_list = [ 'name', 'email_id', 'password', 'gender', 'date_of_birth', 'height', 'weight', 'doctor', 'device', 'dependents', 'caregiver']
        return dict((key, value) for (key, value) in self.__dict__.items() if key in dict_list)

    def add_dependents(self, dep):# dependents is expected to be a list of strings
        if len(self.dependents) < 5:
            if dep not in self.dependents:
                self.dependents.append(dep)
            else:
                print("dependents already exists in list")

        else: 
            print("dependents limit reached")

    def remove_dependents(self, dep):
        if dep in self.dependents:
            self.dependents.remove(dep)
        else: 
            print("dependent not in list")

    
    def print_dependents(self):
        print('dependent list:',self.dependents ) 
        if self.dependents is not None:
            for dep in self.dependents:
                print(dep)
        else:
            print("No dependents")

    def add_caregiver(self, carrer):
        if self.caregiver is None:
            self.caregiver = carrer
        else: 
            print("Already have a caregiver")

    def remove_caregiver(self):
        if self.caregiver is not None:
            self.caregiver = None
        else: 
            print("No caregiver assigned")
            
    def print_caregiver(self):
        if self.caregiver is not None:
            print(self.caregiver)
        else: 
            print("No caregiver")
    


