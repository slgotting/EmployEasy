from tkinter import *
from tkinter import messagebox
import pickle
import itertools
from PIL import Image, ImageTk
import traceback
import random
from itertools import combinations
import cProfile
import csv
import os
import time


root = Tk()


class Person:
    def __init__(self, name, initials, *jobs_can_perform, jobs_training=[]):
        self.name = name
        self.jobs_training = jobs_training
        self.jobs_can_perform = list(jobs_can_perform)
        self.initials = initials

def raise_error(error_msg):
    '''Takes error_msg and creates error dialog box'''

    messagebox.showerror("Error", error_msg)

try:
    people = open("employees.pickle",'rb')
    employees = pickle.load(people)

except IOError as e:
    raise_error('Employees file does not exist. Please run initiation file to create database')

try:
    last_jobs = open("lastjob.pickle",'rb')
    last_jobs = pickle.load(last_jobs)

except IOError as e:
    last_jobs = {}
    





def save_employees():
    pickle_out = open('employees.pickle','wb')
    pickle.dump(employees, pickle_out)
    pickle_out.close()

def save_last_job():
    pickle_out = open('lastjob.pickle','wb')
    pickle.dump(last_jobs, pickle_out)
    pickle_out.close()









person_and_job = {}
list_of_jobs = ['775','875','PP','245','SpotOn','Tester','Accessories','Packaging','RollingCarts']





#*-\/\/\/\/\/\/\/\/\/\/----Not currently in use----\/\/\/\/\/\/\/\/\/\/-*#

class Job:
    def __init__(self, sitting, shoulder_use, heavy_lifting, specialized_task):
        self.sitting = sitting
        self.shoulder = shoulder_use
        self.heavy_lifting = heavy_lifting
        self.specialized_task = specialized_task
        self.requirements = [sitting, shoulder_use, heavy_lifting, specialized_task]

#*---^^^^^^^^^^^^^^^^^^^^^^^^--Not currently in use--^^^^^^^^^^^^^^^^^^^^^^^^---*#








def not_last_job(job,person):

    '''Checks lastjob.pickle db to see if this was their last job'''

    try:
        if job != last_jobs[person.initials]:
            return True
        else:
            return False
    except:
        return True


def can_do_job(job, person):

    '''Returns boolean if person can do the job or not'''
    
    for task in person.jobs_can_perform:
        if job == task:
            return True
    return False


        
def people_who_can_do_job(people,job):

    '''Returns list of people who can do defined job'''
    
    people_who_can_do_job = [person for person in people if can_do_job(job, person)]


    return people_who_can_do_job
    

def needed_people(all_stations_775,all_stations_875,PP,all_stations_245,SpotOn,tester,Accessories,Packaging,RollingCarts):

    '''Needed amount of people for each job'''

    people_needed = {'775':all_stations_775,'875':all_stations_875,'PP':PP,'245':all_stations_245,'SpotOn':SpotOn,'Tester':tester,'Accessories':Accessories,'Packaging':Packaging,'RollingCarts':RollingCarts}
    return people_needed


def get_all_possible_combinations(*args):
    '''For this function we append shorter combinations first so that it usually
        takes less time to find a problem. This could be opposite of what you want
        for different problems, however.'''
    
    total_combinations = []
    i = len(*args) - 1
    while i > 0:
        c = [list(x) for x in combinations(*args, len(*args)-i)]
        total_combinations += c
        i-=1

    return total_combinations


def set_helper_dict(people_available, people_on_job, people_needed, not_last_job=True):

    '''Sets how many people can do each job and how many are needed for each job so that the
        'can_enough_do_every_job' function does not have to call functions repeatedly.'''
    
    helper_dict = {}

    
    for job in list_of_jobs:
        if not_last_job == True:

            current_people_needed = people_needed[job] - people_on_job[job]
            helper_dict[job] = (people_who_can_do_job(people_available,job), current_people_needed)
        else:
            current_people_needed = people_needed[job] - people_on_job[job]
            helper_dict[job] = (people_who_can_do_job(people_available,job), current_people_needed)

    return helper_dict



def can_enough_do_every_job(people_doing_job,job,people_needed,people_on_job,people_available,person):

    '''For the person selected, this function assigns them to the job defined as a parameter. Then it
        goes through every combination of possible jobs and checks to make sure that the total summed
        amount is greater than the total summed needed for those jobs.'''

    people_available.remove(person)
    people_doing_job[job].append(person)
    people_on_job[job] += 1
 
    helper_dict = set_helper_dict(people_available,people_on_job,people_needed)

    i = 0
    
    while i < len(all_combinations):
        temp_list = []
        
        temp_needed = 0
        
        for task in all_combinations[i]:

            temp_list += helper_dict[task][0]
            temp_needed+=helper_dict[task][1]
            
            
        temp_list = list(set(temp_list))
        
      
        if temp_needed > len(temp_list):

            people_available.append(person)
            people_doing_job[job].remove(person)
            people_on_job[job] -= 1
            return False
        else:
            i+=1

    return True
            
    
def get_person_for_job_gen(people_doing_job,people_available,people_needed,people_on_job):

    '''Trys to get people for the job based on if the job was not the last persons job. If it can't,
        it defaults to finding people based on people needed, if they can do the job, and can enough
        people do every job'''

    try:
        try:
            return next((person, job)
                    for person in people_available
                    for job in list_of_jobs
                    if people_needed[job] > people_on_job[job]
                    if not_last_job(job,person)
                    if can_do_job(job,person)
                    if can_enough_do_every_job(people_doing_job,job,people_needed,people_on_job,
                                               people_available,person)
                        )

        except:
            try:
                return next((person, job)
                        for person in people_available
                        for job in list_of_jobs
                        if people_needed[job] > people_on_job[job]
                        if not_last_job(job,person)
                        if can_do_job(job,person)
                        if can_enough_do_every_job(people_doing_job,job,people_needed,people_on_job,
                                                   people_available,person)
                            )
            except:
                
                return next((person, job)
                        for job in list_of_jobs
                        if people_needed[job] > people_on_job[job]
                        for person in people_available
                        
                        if can_do_job(job,person)
                        if can_enough_do_every_job(people_doing_job,job,people_needed,people_on_job,
                                                   people_available,person)
                        )
    except:
        raise_error('There are not enough qualified people for each job to fill this demand')
                     

def fill():

    '''Fills people into jobs by way of generator function 'get_person_for_job_gen' and returns them'''
    
    global total_needed
    global people_with_job_already
    people_with_job_already = []
    

        
    people_on_job = {'775':0,'875':0,'SpotOn':0,'Accessories':0,'Packaging':0,'RollingCarts':0,'PP':0,'245':0,'Tester':0}
    people_doing_job = {'775':[],'875':[],'SpotOn':[],'Accessories':[],'Packaging':[],'RollingCarts':[],'PP':[],'245':[],'Tester':[]}
    
    available_people = [person for person in all_people if person not in people_with_job_already]
    
    i = 0
    
    
    while total_needed > 0:
        
        
        person, job = get_person_for_job_gen(people_doing_job,available_people,people_needed,people_on_job)
        

        person_and_job[person] = job

        people_with_job_already.append(person)
        
        available_people = [person for person in all_people if person not in people_with_job_already]
        

        i+=1
        total_needed-=1
    
            
    return people_on_job, people_doing_job, available_people, person_and_job
        

                

def are_jobs_filled():
    
    available_people = [person for person in all_people if person not in people_with_job_already]
    
    total_needed = 0
    
    for job in people_needed:
        total_needed += people_needed[job]


    if len(people_with_job_already) == total_needed:
        return True
    else:
        return False

        
def find_fit():
    i=0
    global total_needed
    total_needed = 0
    
    for job in people_needed:
        total_needed += people_needed[job]

    if len(all_people) < total_needed:
        raise_error('Not enough people to meet this request')
        return False

    random.shuffle(all_people)

    people_doing_job, people_on_job, available_people, person_and_job = fill()
  
    if are_jobs_filled() == True:
        return people_doing_job, people_on_job, available_people, person_and_job
    else:
        people_with_job_already = []
    print('There is not an orientation to match this demand')


def assign_jobs(employees, needed, no_of_schedules):
    
    global person_and_job
    global last_jobs
    global all_combinations
    global people_needed
    global all_people

    all_combinations = get_all_possible_combinations(list_of_jobs)

    created = 0
    
    all_people = list(employees.values())
    
    person_and_job_dict = {}

    for person in all_people:
        person_and_job_dict[person] = [person.name, person.initials]

    
    while created < no_of_schedules:
        
        person_and_job = {}
        
        try:
            last_jobs = open('lastjob.pickle','rb')
            last_jobs = pickle.load(last_jobs)
        except:
            last_jobs = {}
            save_last_job()

        people_needed = needed_people(*needed)

        y = 0
        while y < random.randint(1,100):
            random.shuffle(all_people)
            y+=1
            
        how_many_doing_same_job = len(all_people)
        j=2
        k=0
 
        while how_many_doing_same_job >= j:
            k=0
            while k < 20:
            
                how_many_doing_same_job = 0
            
                people_doing_job, people_on_job, available_people, person_and_job = find_fit()
                for person in person_and_job:
                    try:
                        if last_jobs[person.initials] == person_and_job[person]:
                            how_many_doing_same_job+=1
                    except:
                        pass
                
                if how_many_doing_same_job < j:
                    break
                k+=1
            j+=1

        created+=1

        for person in person_and_job:
            last_jobs[person.initials] = person_and_job[person]

        for person in available_people:
            last_jobs[person.initials] = ''

        save_last_job()

        for person in all_people:
            person_and_job_dict[person].append(last_jobs[person.initials])

        
    new_dict = {}
    temp_list = []

    for person in person_and_job_dict:
        temp_list.append(person.initials)

    temp_list = sorted(temp_list)


    for initials in temp_list:
        for person in person_and_job_dict:
            if initials == person.initials:
                new_dict[initials] = person_and_job_dict[person]


    try:
        os.remove('Schedule.csv')
    except:
        print('File does not exist')
            
    try:
        with open('Schedule.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for person in new_dict:
                writer.writerow(new_dict[person])
    except:
        raise_error("Please close the file 'Schedule.csv' and try again")
            
            



#--------------------------------------GUI Section--------------------------------------#


def delete_person(person):

    '''Deletes person from db and reloads GUI.'''
    
    if person.initials in employees: del employees[person.initials]
    if person.initials in last_jobs: del last_jobs[person.initials]

    save_employees()
    save_last_job()

    sort_by_name()

def really_delete(person):

    '''Checks to see if you really want to delete said person.'''
    
    delete_window = Toplevel()

    sure = Label(delete_window,text='Are you sure you want to delete this employee?')
    sure.grid(row=0,column=0,columnspan=4)

    yes = Button(delete_window,text='Yes',command=lambda p=person: delete_person(p))
    yes.grid(row=1,column=0,columnspan=2,sticky='nsew')

    no = Button(delete_window,text='No',command= lambda: delete_window.destroy())
    no.grid(row=1,column=2,columnspan=2,sticky='nsew')
    
    
def new_employee(name, initials):
    
    '''Adds employee to the database.'''
    
    if initials in employees:
        raise_error("Employee already exists")
    else:
        employees[initials] = Person(name, initials)

        save_employees()

        sort_by_name()
        
    
def add_employee_dialog():
    
    '''Window that pops up, allowing user to enter employee name and initials,
        so that they are added to the database.'''
    
    add_window = Toplevel()

    add_employee = Label(add_window,text='Add An Employee')
    add_employee.grid(row=0,column=0,columnspan = 2)

    name_label = Label(add_window, text='Name:')
    name_label.grid(row=1,column=0,sticky='e')

    initials_label = Label(add_window, text='Initials:')
    initials_label.grid(row=2,column=0,sticky='e')

    name = Entry(add_window)
    name.grid(row=1,column=1,sticky='nsew')

    initials = Entry(add_window)
    initials.grid(row=2,column=1,sticky='nsew')
    

    add = Button(add_window, text='Add',
                 command= lambda: new_employee(name.get(), initials.get()))
    add.grid(row=3,column=0,columnspan=2)


def save_changes(name, initials, person):

    '''Saves the changes made to an employees initials and name.'''
    
    if person.initials in employees: del employees[person.initials]
    employees[str(initials)] = person
    employees[str(initials)].name = str(name)
    employees[str(initials)].initials = str(initials)
    
    save_employees()

    sort_by_name()


def edit_employee(person):

    '''The window that opens, allowing edits to name and initials.'''
    
    window = Toplevel()
    
    L = Label(window,text='Edit Employee')
    L.grid(row=0,column=0,columnspan=2)
    name_label = Label(window,text='Name:')
    name_label.grid(row=1,column=0)
    
    initials_label = Label(window,text='Initials:')
    initials_label.grid(row=2,column=0)
    
    name = Entry(window)
    name.insert(END, person.name)
    name.grid(row=1,column=1)
    
    initials = Entry(window)
    initials.insert(END, person.initials)
    initials.grid(row=2,column=1)
    
    save = Button(window, text='Save',
            command= lambda: save_changes(name.get(),initials.get(),person))
    save.grid(row=3, column=0,columnspan=2)


def job_button(btn, job, person):

    '''Functionality for clicking on each job button for each person, gets passed in a person and job,
        and adjusts it accordingly based on the colors.'''

    if btn['bg'] == 'red':
        btn.configure(bg='yellow')
        person.jobs_training.append(job)
    elif btn['bg'] == 'yellow':
        btn.configure(bg='green')
        person.jobs_training.remove(job)
        person.jobs_can_perform.append(job)
    elif btn['bg'] == 'green':
        btn.configure(bg='red')
        person.jobs_can_perform.remove(job)

    save_employees()
    

def sort_by_name(create=True):

    '''Creates the job and person button grid and sorts it by name.'''

    global employees
    new_dict = {}
    temp_list = []

    for person in employees:
        temp_list.append(employees[person].initials)

    temp_list = sorted(temp_list)

    for initials in temp_list:
        for person in employees:
            if initials == employees[person].initials:
                new_dict[initials] = employees[person]

    employees = new_dict
    if create == True:
        create_main()
    
def sort_by_job(job):

    '''Sorts employees alphabetically by given job and if they can do said job.'''
    
    sort_by_name(create=False)
    global employees
    can_do = []
    cant_do = []
    new_dict = {}
    for person in employees:
        if job in employees[person].jobs_can_perform:
            can_do.append(employees[person])
        else:
            cant_do.append(employees[person])

    temp_list = can_do + cant_do
    for person in temp_list:
        new_dict[person.initials] = person

    employees = new_dict

    create_main()


def pass_needed_and_generate(needed, no_of_schedules):

    '''Calls the main function to create the schedule.'''

    needed_entrys = [int(i.get()) for i in needed if i != '']

    assign_jobs(employees, needed_entrys, int(no_of_schedules))


def create_main():

    '''Main GUI window'''
    
    global root
    root.destroy()
    root = Tk()
    
    close_btn = Image.open('close-window.jpg')
    close = ImageTk.PhotoImage(close_btn)

    plus_btn = Image.open('plus.jpg')
    plus = ImageTk.PhotoImage(plus_btn)

    employee_buttons = []
    job_btns = []
    job_and_person_btns = []
    delete_buttons = []


#*---------------------\/----People Needed and generate job function---\/----------------------------------*#


    needed = Label(root, text='Enter people needed for each job in fields below')
    needed.grid(row=2, column=50, padx = 30, columnspan=2)


    needed_labels = []
    needed_entrys = []

    for i, j in enumerate(list_of_jobs):
        needed_labels.append(Label(root, text = j + ":"))
        needed_labels[i].grid(row = i+4, column=50, padx=30,sticky='e')

        needed_entrys.append(Entry(root, width=5))
        needed_entrys[i].grid(row = i+4, column=51, sticky='w')
        needed_entrys[i].insert(END, '2')

        

    how_many_label = Label(root,text='How many days/schedules to create:')
    how_many_label.grid(row =len(needed_labels) + 5, column=50)
    how_many = Entry(root, width=5)
    how_many.grid(row=len(needed_labels) + 5, column=51)
    how_many.insert(END, '1')
    
    

    generate = Button(root,text='Generate Job Placement',
                      command = lambda: pass_needed_and_generate(needed_entrys, how_many.get()))
    generate.grid(row=len(needed_labels) + 7, column=50, padx = 30, columnspan=2)


#*--------------------^^-----People Needed and generate job function---^^----------------------------------*#




    sort_by_name_btn = Button(root,text='Name',command=sort_by_name)
    sort_by_name_btn.grid(row=1, column=2, sticky='nsew')

    for i, o in enumerate(employees):
        delete_buttons.append(Button(root,image=close,
                                    command= lambda p=employees[o]: really_delete(p)))
        delete_buttons[i].grid(row=i+2,column=1,sticky='nsew')
        
        employee_buttons.append(Button(root,text=employees[o].name,
                               command= lambda p=employees[o]: edit_employee(p)))
        employee_buttons[i].grid(row=i+2, column=2,ipady=1, sticky='nsew')

        j = 0
        while j < len(list_of_jobs):
            if list_of_jobs[j] in employees[o].jobs_can_perform:
                color = 'green'
            elif list_of_jobs[j] in employees[o].jobs_training:
                color = 'yellow'
            else:
                color = 'red'
            btn = Button(root,text =list_of_jobs[j] +  ', ' + employees[o].initials, bg=color)
            btn.configure(command = lambda b=btn, i=list_of_jobs[j], j=employees[o]: job_button(b, i, j))
            job_and_person_btns.append(btn)
            

            job_and_person_btns[j+(i*9)].grid(row=i+2, column=j+3, ipady=1, sticky='nsew')
            j+=1


    for i, o in enumerate(list_of_jobs):
        job_btns.append(Button(root,text = o, width = 10,
                                command = lambda j=list_of_jobs[i]: sort_by_job(j)))
        job_btns[i].grid(row=1, column= i+3, ipady=4, sticky='ew')


    add_btn = Button(root,image=plus,
                    command = add_employee_dialog)
    add_btn.grid(row=len(employee_buttons)+2, column=2,sticky='nsew')

    
    root.mainloop()
    
sort_by_name()































