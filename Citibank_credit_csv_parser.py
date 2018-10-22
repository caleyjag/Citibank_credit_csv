# -*- coding: utf-8 -*-
"""

Little tool for me to add a column of accumulated total debit on my 
Citibank credit card .csv statement

Not optimized to be pythonic since it's just for me!

Created on Sun Oct 21 12:38:48 2018
@author: gmilne
"""

import numpy as np
import csv

data_array = ['1','1','1','1','1'] #this is for array iniatization and will be deleted later

with open('MC_538_092116_102018.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
                
                #append to master list
                data_array = np.vstack((data_array, row))
        data_list=list(csv.reader(f, delimiter = ',')) #convert the csv reader output into a more useful list             


data_array_header = data_array[1]
data_array = data_array[2:]  #slice off the first two rows (initialization and table header)
debits = data_array[:, 3]
credit = data_array[:, 4] #can't use 'credits' since that is a keyword


array_size = len(data_array[:,0])


total_debit = np.zeros(array_size)
running_total = float(0)
for i in range(0, array_size):
    debit_string = debits[(array_size-1)-i]
    credit_string = credit[(array_size-1)-i]
    if not debit_string:  #looking for case where debit field is empty. A credit must have been made
        
        if credit[(array_size-1)-i]:
            #check if both credit and debit strings are empty in which case do nothing. This appears to be rare but can happen for Citi transactions like 'MEMBERSHIP FEE'
            #if credit field is not empty we need to subtract it from our current debit running total
            credit_string = credit_string.replace(',', '')
            running_total = running_total - float(credit_string)
                
    else:
        #add the debit to the current debit running total
        debit_string = debit_string.replace(',', '')
        running_total = running_total + float(debit_string)
    total_debit[(array_size - 1) - i] = running_total    
   
print(total_debit)    

x_arrstr = np.char.mod('%0.2f', total_debit)
x_str = "\n".join(x_arrstr)
print(x_str)    


#need to add in save to .csv
