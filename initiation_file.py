import pickle


class Person:
    def __init__(self, name, initials, *jobs_can_perform, jobs_training=[]):
        self.name = name
        self.jobs_training = list(jobs_training)
        self.jobs_can_perform = list(jobs_can_perform)
        self.initials = initials

sure = input('Are you sure you want to run this file? It will reset all employees to the defaults as outlined in this file (y/n) ')

if sure == 'y':
    employees = {
        'SG1': Person('Steven','SG1','775','875','Accessories','PP','Packaging','RollingCarts'),
        'RC': Person('Paulie','RC','Accessories','Packaging'),
        'IE': Person('Isaac','IE','Accessories','Packaging','RollingCarts'),
        'MM3': Person('Marcia','MM3','775','875','SpotOn'),
        'JC': Person('Jose','JC','775','875','SpotOn'),
        'NC': Person('Noni','NC','245','SpotOn'),
        'DD': Person('David','DD','775','PP','875','Accessories','Packaging','RollingCarts'),
        'SB': Person('Samantha','SB','775','SpotOn','875'),
        'DL': Person('David','DL','Accessories','Packaging','RollingCarts'),
        'RS': Person('Rodison','RS','775','SpotOn','875'),
        'SLL': Person('Samuel','SLL','775','875','Accessories','RollingCarts','145','245'),
        'JA1': Person('Jerry','JA1','775','875','Accessories','Packaging','RollingCarts','PP'),
        'JG': Person('Joyce','JG','Accessories','SpotOn'),
        'EG': Person('Eurola','EG','Accessories','Packaging','SpotOn'),
        'AI': Person('Ahmed','AI','Accessories','Packaging','RollingCarts'),
        'EG': Person('Ernest','EG','Accessories','Packaging','RollingCarts'),
        'LA': Person('Lea','LA','775','875','SpotOn','Tester'),
        'FG': Person('Fernando','FG','775','875','SpotOn','Tester','PP'),
        'TA': Person('Teresa','TA','775','875','SpotOn','Tester'),
        'RR': Person('Regina','RR','775','Accessories','SpotOn'),
        'JA4': Person('Joe','JA4','775','875','Accessories','Packaging','SpotOn'),
        'JA3': Person('Keith','JA3','775','875','PP','245','Packaging'),
        'BA': Person('Benson','BA','Accessories','Packaging','RollingCarts'),
        'TT': Person('Thanh','TT','775','875','SpotOn','245'),
        'KK': Person('Kong','KK','775','875','SpotOn'),
        'SS': Person('Sokha','SS','775','875','SpotOn'),
        'PP': Person('Pow','PP','Accessories','Packaging','RollingCarts'),
        'TG': Person('Tigi','TG','245','Tester'),
    }

    pickle_out = open('employees.pickle','wb')
    pickle.dump(employees, pickle_out)
    pickle_out.close()
