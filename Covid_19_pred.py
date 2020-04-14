'Author: DHEERAJ'
'Date: 10-04-2020'
'Data Analysis and predictions on Covid 19 Data in various countries'


#specify a start date from which pred algo shall be trained with recorded data#

start_date='2020-03-01'
################# specify no:of future days to be predicted ###################

forcast_days = 3
######### specify countries interested starting with capital letter############

countries =['India','United States','Germany','Italy','World']

###############################################################################
#################################### Code #####################################
###############################################################################
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
#import matplotlib.gridspec as gridspec

############################### reading csv file #############################
df=pd.read_csv('full_data.csv')

###################### defining columns as array variables ###################
date=df.date
location=df.location
total_cases=df.total_cases
total_deaths=df.total_deaths



############################################################################## 
############# major filter for countries and their related data ##############
##############################################################################

countries_data=[]

#countries_data = [c_d0, c_d1......, c_dn]
#c_d=[countries[q],selected_dates1, all_dates, selected_cases1, yFit1, selected_deaths1, f_rate]

for q in range(0,len(countries)):
    country_id1=[]
    country_dates1=[]
    i=0
    for i in range(len(location)):
        if location[i]==countries[q]:
            country_id1.append(i)
            country_dates1.append(date[i]) 
            i+=1
    
    ####################### filtering wrt start date ##########################
    selected_country_date_id1=[]
    j=0
    for j in range(len(country_dates1)):
        if country_dates1[j]==start_date:
            selected_country_date_id1.append(j)
            j+=1
    
    k=int(selected_country_date_id1[0])
    selected_dates1=country_dates1[k:]
    
    ####### #retrieving cases and deaths wrt country1 and selected dates ######
    selected_cases1=[]
    selected_deaths1=[]
    
    if date[country_id1[k]]==start_date:
        for l in range(k,len(country_dates1)):
            selected_cases1.append(total_cases[country_id1[l]])
            selected_deaths1.append(total_deaths[country_id1[l]])
            l+=1
    
       
    
    ######################## Countries prediction #############################
    def cases(x, a, b, c, d, e):
        return a*x**4+b*x**3+c*x**2+d*x+e   
    
    xD = np.arange(1,len(selected_dates1)+1,1)
    yD = selected_cases1
    
    popt, pcov = curve_fit(cases, xD, yD)
    #print(popt)
    
    xFit = np.arange(1,len(selected_dates1)+1+forcast_days,1)
    yFit = cases(xFit, *popt)
    
    future_dates = []
    last_date=selected_dates1[-1]
    last_d=int(last_date[8:10])
    last_m= int(last_date[5:7])
    if last_m % 2 == 0:
             v=30
    else:
        v=31
    
    for i in range(1,forcast_days+1):
         u = str(last_date[0:8])+str(last_d+i)
         future_dates.append(u)
        
    all_dates = selected_dates1 + future_dates
    yFit1 = [] 
    for i in range(0,len(yFit)):
        n = int(yFit[i])
        yFit1.append(n)
        
    ############################# Fatality rate ##############################
    
    f_r = (selected_deaths1[-1]/selected_cases1[-1])*100
    f_rate = round(f_r, 2)

    ######################### Countries complete data set ####################
    c_d=[countries[q],selected_dates1, all_dates, selected_cases1, yFit1, selected_deaths1, f_rate] 
    countries_data.append(c_d)
    q+=1

##############################################################################
############################## Plotting ######################################
##############################################################################
'Master data is available now in - countries_data'

for i in range(0,len(countries)):      
    fig = plt.figure(figsize=(16,16))
    ax = plt.subplot()
    plt.xticks(rotation=90)   
    
    plt.plot(countries_data[i][1],countries_data[i][5],'ro',label= countries[i]  + ' Recorded deaths')
    plt.plot(countries_data[i][1],countries_data[i][3],'bo',label= countries[i]  + ' Recoreded cases')
    plt.plot(countries_data[i][2],countries_data[i][4],'r--',label= countries[i] +' Predicted cases')
    
    plt.xlim(len(countries_data[i][2])-15, len(countries_data[i][2]))
    
    plt.title('Covid 19 - '+ str(forcast_days)+ ' day' ' predicted cases in '+ 
               countries[i]  + ' on ' + all_dates[-(forcast_days)], fontsize=28)
    
    ax.tick_params(labelcolor='k', labelsize='xx-large')
    
    plt.minorticks_on()
    plt.grid(b=True, which='major', color='lightgray', linestyle='-')
    plt.xlabel('Days',fontsize=24)
    plt.ylabel('Count',fontsize=24)
    
    bbox_args1 = dict(boxstyle="square", fc="1")
    bbox_args2 = dict(boxstyle="square", fc="0.9")
    arrow_args = dict(arrowstyle="->")
    
    anX1 = countries_data[i][2][-forcast_days:-(forcast_days-1)]+countries_data[i][2][-2:]
    anY1 = countries_data[i][4][-forcast_days:-(forcast_days-1)]+countries_data[i][4][-2:]
    
    anX2 = countries_data[i][1][-2:]
    anY2 = countries_data[i][3][-2:]
    
    # to call out data points
    # for xy in zip(anX1,anY1):
    #       ax.annotate('Pred: %s --- %s cases' % xy, 
    #                   xy=xy,
    #                   horizontalalignment='right',
    #                   bbox=bbox_args1,
    #                   arrowprops=arrow_args, 
    #                   xytext=(-30, -100),textcoords='offset points',fontsize=12)
    # for xy in zip(anX2,anY2):
    #       ax.annotate('Rec: %s --- %s cases' % xy, 
    #                   xy=xy,
    #                   horizontalalignment='left',
    #                   bbox=bbox_args2,
    #                   arrowprops=arrow_args, 
    #                   xytext=(100, -80),textcoords='offset points',fontsize=12)
    
    ax.text(len(countries_data[i][2])*0.867,int(countries_data[i][4][-1]/2.5), 
            r'Recorded Cases: '+'\n'+'Dates = '+str(anX2)+'\n'+'Cases = '+str(anY2), 
            fontsize=18,bbox=bbox_args1)
    
    ax.text(len(countries_data[i][2])*0.82,int(countries_data[i][4][-1]/4), 
            r'Predicted Cases: '+'\n'+'Dates = '+str(anX1)+'\n'+'Cases = '+str(anY1), 
            fontsize=18,bbox=bbox_args1)
    
    
    ax.text(len(countries_data[i][2])*0.92,int(countries_data[i][4][-1]/6), 
            r'Fatality rate: '+str(countries_data[i][6])+' %', 
            fontsize=18,bbox=bbox_args1)
    
    plt.legend(fontsize=18)
    i+=1

plt.show()













