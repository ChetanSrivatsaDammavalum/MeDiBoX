import CustomerDatabaseService as cds

class login:
    def __init__(self, email_id = None, password = None, success_e = False, success_p = False):
        self.email_id = email_id 
        self.password = password
        self.success_e = success_e
        self.success_p = success_p

    def check_email(self,df):
        self.success_e = cds.check_customerdata_from_file(df,'email_id',self.email_id)
        return self.success_e
    
    def check_password(self,df):
        self.success_p = cds.check_specific_customerdata_from_file(df,'email_id',self.email_id,'password',self.password)
        return self.success_p

class registration(login):
    def __init__(self, email_id, success_e = True):
        super().__init__( email_id, success_e)
    
    def check_email(self,df):
        self.success_e = cds.check_customerdata_from_file(df,'email_id',self.email_id)
        return self.success_e
    
class caretaker_service:
    # def __init__(self,uc):
    def view_dependents(self, uc):
        return uc.print_dependents(uc)     

    def check_dependents(self, df,dep):
        success_d = False
        success_d = cds.check_customerdata_from_file(df,'name',dep)
        return success_d

    def add_dependents(self,uc, dep):
        return uc.add_dependents(uc, dep)

    def remove_dependents(self,uc, dep):
        return uc.remove_dependents(uc, dep)

class dependents:
    #def __init__(self,uc):
    def view_caretaker(self, uc, dep):
        return uc.print_dependents(dep)     
    
    def add_caretaker(self,uc, dep):
        return uc.add_dependents(dep)

    def remove_caretaker(self,uc, dep):
        return uc.remove_dependents(dep)
    
class prescription_service: 
    def print_prescription(self, pd):
        #"""
        for medicine in pd:
            #print(' medicine in prescription service: \n',medicine)
            medicine.print_priscription(medicine) 
        return None
        #"""