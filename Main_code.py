# dataset source: https://data.gov.uk/dataset/c0eec478-ef19-4234-826f-8efb9563eda2/road-safety
import pandas as pd
import matplotlib.pyplot as plt

df1=pd.read_csv('/Users/Documents/accidents.csv')
print('Number of rows & columns: ',df1.shape)
#print(df1.columns)
#Cleaning column labels
df1.columns=map(str.lower,df1.columns) # Change the column names to lowercase
# Make some column names shorter
df1=df1.rename(index=str, columns={"pedestrian_crossing-physical_facilities'": "pedestrian_cpf",
                                   "did_police_officer_attend_scene_of_accident": "police_attendance"})

# Changed the format to DatetimeIndex in Pandas
df_date=pd.DatetimeIndex(df1['date']) # Access df by df.year/df.month/df.day


# value_count_calculator function finds the frequency of each unique value in the series_input.
# This function organizses the value counts (corresponds to cases) in a new dataframe.
def value_count_calculator(series_input,name_input_str,index_name_str): # name_input_str = 'cases', index_name_str = label (str) for series_input
    df_temp1=pd.DataFrame({name_input_str: series_input.value_counts()})
    df_temp1[index_name_str]=df_temp1.index #Assigning the index to a series
    df_temp1=df_temp1.sort_values(by=[index_name_str])
    return df_temp1
# Sums the values in the series_input for each year
def sum_calculator(series_input,name_input_str):
    df_temp=pd.DataFrame({name_input_str: series_input.groupby(df_date.year).sum()})
    df_temp['year']=df_temp.index #Assigning the index to a series
    df_temp=df_temp.sort_values(by=['year'])
    return df_temp

cases_per_year=value_count_calculator(df_date.year,'cases','year')
casualties_per_year=sum_calculator(df1['number_of_casualties'],'casualties')
vehicles_per_year=sum_calculator(df1['number_of_vehicles'],'vehicles')
# Plot 1
fig, ax = plt.subplots()
ax.plot(cases_per_year['year'],cases_per_year['cases'], c = 'b' , label = 'Cases')
ax.set_xlabel('Year') # plt.xlabel
ax.set_ylabel('Total')
ax.set_ylim(bottom=0, top=1200) # plt.ylim
ax.set_xlim(right=2018)
ax.plot(casualties_per_year['year'],casualties_per_year['casualties'],c= 'r', label = 'Casualties')
ax.plot(vehicles_per_year['year'],vehicles_per_year['vehicles'],c= 'g', label = 'Vehicles')
ax.legend(['Cases','Casualties','Vehicles'],loc=4)
ax.spines['right'].set_visible(False) # plt version?
ax.spines['top'].set_visible(False)
ax.set_title('Number of cases/casualties/vehicles from 2005-2017') # plt.title
plt.savefig('/Users/arian/Documents/Pictures/Cases_casualties_vehicles_2005_to_2017.png')
plt.show()
######## Cases per day of week and month #######

# Creating a separate column for year, month and day
df1['year']=df1['date'].str.slice(start=6).astype(int) # Extract year from str and changed to int
df1['month']=df1['date'].str.slice(start=3,stop=-5).astype(int) # Extract month from str and changed to int
df1['day']=df1['date'].str.slice(start=0,stop=-8).astype(int) # Extract day from str and changed to int 
#Day of week
cases_per_dow=value_count_calculator(df1['day_of_week'],'cases','dow')
days_of_week_map={1:'Sunday', 2:'Monday', 3:'Tuesday', 4:'Wednesday', 
                  5:'Thursday', 6:'Friday', 7:'Saturday'}
cases_per_dow['dow_new']=cases_per_dow['dow'].map(days_of_week_map)
#Month
cases_per_month=value_count_calculator(df1['month'],'cases','month')
month_map={1:'January', 2:'February', 3:'March', 4:'April', 
                  5:'May', 6:'June', 7:'July', 8:'August',9:'September',
                  10:'October', 11:'November', 12:'December'}
cases_per_month['month_new']=cases_per_month['month'].map(month_map)
# Plot 2
fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10,10))
ax1.bar(cases_per_dow['dow_new'],cases_per_dow['cases'])
ax1.set_ylim(bottom=0, top=1100)
ax1.set_ylabel('Cases')
ax1.spines['right'].set_visible(False) # plt version?
ax1.spines['top'].set_visible(False)
ax1.set_title('Number of cases per day of week from 2005-2017',fontsize=14)
ax2.bar(cases_per_month['month_new'],cases_per_month['cases'])
ax2.set_ylim(bottom=0, top=700)
ax2.set_ylabel('Cases')
ax2.spines['right'].set_visible(False) # plt version?
ax2.spines['top'].set_visible(False)
ax2.set_title('Number of cases per month from 2005-2017', fontsize=14)
plt.xticks(rotation=90) # Doesn't work with ax
plt.savefig('/Users/Documents/Data science project/Pictures/Cases_wrt_month&dow.png')
plt.show()
