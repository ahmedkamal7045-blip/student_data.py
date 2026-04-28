
import csv
import os
from datetime import timedelta,datetime   
import time

import threading

def department_specialization()->str:
    departments_specializations={'Engineering':('Mechanical', 'Electrical', 'Computer', 'Architectural'),
                 'Maritime Studies': ('Marine Engineering', 'Sea Training'),
                 'Business/Management': ('Marketing', 'Finance', 'Logistics'),
                 'Computing': ('Information Systems', 'Computer Science')}
    
    print(f"write 'yes' when you see your department")
    try:
        for department,specializations in departments_specializations.items():
        
            dep=input(f" {department} \n yes  no\n")
            
            if dep.lower() =='yes':
                print(f"write 'yes' when you see your specialization")
                for specialization in specializations:
                     spe=input(f" {specialization} \n yes  no\n")
                     if spe.lower()=='yes':
                          return f"{department} - {specialization}"
            
        raise ValueError("we will set unknown department for now you can update later")
    except ValueError as e:
        print(e)
        return f"unknown department"

    
    
class DomainError(ValueError):
    pass



def student_info()->dict[str,str]:
    stu_dict_info={}
    name=input('your full name: ')
    if name=='' or name.isspace():
        name='no name'
    stu_dict_info['name']=name
    department=department_specialization()
    stu_dict_info['department']=department
    for try_t in range(3):
        try:
           academic_year=int(input(f'your academic year {list(range(2011,2061))}\n' ))
           if academic_year not in range(2011,2061):
               raise DomainError(' we only accept academic year from 2011 to 2060 ')
           stu_dict_info['academic_year']=academic_year
           break
        except DomainError as e:
            print(f'{e} try again')
            
        except ValueError:
            print('enter a number')
            
    else:
        stu_dict_info['academic_year']=9999
    return stu_dict_info

 
#database=[]    
class Student:
    student_id=0
    database=[]
    def __init__(self,stud_info:dict[str,str]):
        for key,val in stud_info.items():
            setattr(self,key,val)
        self.student_id=Student.student_id
        Student.student_id+=1
        self.creation_date=datetime.today()
        self.student_data={'student_id':self.student_id,'name':self.name,'department':self.department,'academoc_year':self.academic_year,'date of input':self.creation_date}
        
    def set_data(self):
        self.database.append(self.student_data)
    
    def update_name(self):
        if datetime.today()>=self.creation_date+timedelta(days=30,seconds=10):
                print('you can not change old data but you can create new data with new id')
                return f'Good luck'
                        
        
        self.name=input('your new name')
        self.student_data['name']=self.name
        for student in self.database:
            if student['student_id']==self.student_id:
                student['name']=self.name
                return f'Mission complete your new name is {self.name}'
        else:
            raise ValueError("you did not set the data, set it first")

    def update_department_specialization(self):
        
        if datetime.today()>=self.creation_date+timedelta(days=30,seconds=10):
                print('you can not change old data but you can create new data with new id')
                return f'Good luck'
        
        self.department_specialization=department_specialization()
        for student in self.database:
            if student['student_id']==self.student_id:
                student['department']=self.department_specialization
                return f'Mission complete your new department is {self.department_specialization}'
        else:
            raise ValueError("you did not set the data, set it first")

    def update_academic_year(self):
        
        if datetime.today()>=self.creation_date+timedelta(days=30,seconds=2):
                print('you can not change old data but you can create new data with new id')
                return f'Good luck'
        

        try:
            self.academic_year=int(input(f'academic year {list(range(2011,2061))}\n' ))
            if self.academic_year not in range(2011,2061):
               raise DomainError(' we only accept academic year from 2011 to 2060 ')
        except DomainError as e:
            
            self.academic_year=9999#default
            
            return f'{e} try again later '
        except ValueError:
            
            self.academic_year=9999#default
            return 'you have to enter a number try later'
        for student in self.database:
            if student['student_id']==self.student_id:
                student['academic_year']=self.academic_year
                return f'Mission complete your new department is {self.department_specialization}'
        else:
            raise ValueError("you did not set the data, set it first")

    def retrieve_data_f_file(self,f_name):
             '''Retrive data using student object'''
             with open(f_name,'r') as f:
                 reader=csv.reader(f)
                 for line in reader:
                     try:
                        if line[0]==self.student_id:
                             print(line)
                     except IndexError as e:
                        print(f"u pumped into empty row {e} ")
file_name='student.csv'
def send_to_file(file_name, flag):
    while not stop_flag.is_set():
         if Student.database:
              stud_data_fr_databa=Student.database[-1]
              if datetime.today()>=stud_data_fr_databa['date of input']+timedelta(days=30):
                      del Student.database[-1]
                      with open(file_name,'a+',newline='') as f:
                            f.seek(0)
                            is_empty=f.read()==''
                            f.seek(0,os.SEEK_END)
                            file_handle=csv.writer(f)
                            if is_empty:
                                header=[key for key in st_data_fr_databa]
                                file_handle.writerow(header)
                            row_s_info=[stud_data_fr_databa.get(key, '') for key in stud_data_fr_databa.keys()]
                            file_handle.writerow(row_s_info)
         else:
                 time.sleep(29*24*60*60)


stop_flag=threading.Event()
thread_th=threading.Thread(target=send_to_file,args=(file_name,stop_flag))
thread_th.start()


def retrieve_data_f_file(f_name,stud_ID):
             '''Rtrieve data using only id'''
             with open(f_name,'r') as f:
                 reader=csv.reader(f)
                 for line in reader:
                     try:
                        if line[0]==str(stud_ID):
                             print('  '.join(line))
                             break
                     except IndexError as e:
                        print(f"u pumped into empty row {e} ")
                 else:
                     print('Wrong ID')


def update_data_file_after_sending(f_name,stud_obj):
    with open(f_name,'r', newline='') as f:
        updated_data=[]
        reader=csv.reader(f)
        for line in reader:
            if line[0]==str(stud_obj.student_id):
                for item in ['name','department','academoc_year']:
                    print(f'Do want to update {item}')
                    answer=input('write yes if that what you want to update\n')
                    if answer.lower()=='yes':
                        new_data=input('Enter new data: ')
                        if item=='academoc_year':
                            new_data=int(new_data)
                        stud_obj.student_data[item]=new_data
                line=[stud_obj.student_data.get(k, '') for k in stud_obj.student_data]
            updated_data.append(line)
    with open(f_name,'w',newline='') as f:
        writer_obj=csv.writer(f)
        writer_obj.writerows(updated_data)
            
                
                
        
s1_inf=student_info()
#print(s1_inf)
s1=Student(s1_inf)
#print(s1.name,s1.department,s1.student_id,s1.academic_year)

#s1.set_data()
#try:
#    s1.update_name()
#except ValueError as e:
#    print(e)
s1.set_data()
#print(Student.database)
#print(s1.name,s1.department,s1.student_id,s1.academic_year)
#try:
#    s1.update_department_specialization()
#except ValueError as e:
#    print(e)
#print(s1.name,s1.department,s1.student_id,s1.academic_year)
#try:
#    s1.update_academic_year()
#except ValueError as e:
#    print(e)
#print(s1.name,s1.department,s1.student_id,s1.academic_year)
#s2_inf=student_info()
#s2=Student(s2_inf)
#print(Student.database)
#s2.set_data()
#print(Student.database)

#send_to_file(file_name)
#s1.retrieve_data_f_file(file_name)
update_data_file_after_sending('studenttt data.csv',s1)

retrieve_data_f_file('studenttt data.csv',0)

stop_flag.set()
thread_th.join()        
retrieve_data_f_file('studenttt data.csv',1)
