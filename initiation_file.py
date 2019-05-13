import pickle


class Person:
    def __init__(self, name, initials, *jobs_can_perform, jobs_training=[]):
        self.name = name
        self.jobs_training = list(jobs_training)
        self.jobs_can_perform = list(jobs_can_perform)
        self.initials = initials

sure = input('Are you sure you want to run this file? It will reset all employees to the defaults as outlined in this file (y/n) ')

if sure == 'y':
    SG1 = Person('Steven','SG1','775','875','Accessories','PP','Packaging','RollingCarts')
    RC = Person('Paulie','RC','Accessories','Packaging')
    IE = Person('Isaac','IE','Accessories','Packaging','RollingCarts')
    MM3 = Person('Marcia','MM3','775','875','SpotOn')
    JC = Person('Jose','JC','775','875','SpotOn')


    employees = {'SG1':SG1, 'RC':RC, 'IE':IE, 'MM3':MM3, 'JC':JC}

    
    
    pickle_out = open('employees.pickle','wb')
    pickle.dump(employees, pickle_out)
    pickle_out.close()
