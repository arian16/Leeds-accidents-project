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
plt.savefig('/Users/Pictures/Cases_casualties_vehicles_2005_to_2017.png')
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
plt.savefig('/Users/Pictures/Cases_wrt_month&dow.png')
plt.show()


######### Cases per weather catergory and speed limit #######
cases_per_weather=value_count_calculator(df1['weather_conditions'],'cases','weather')
cases_per_speed=value_count_calculator(df1['speed_limit'],'cases','speed')

fig3, ax3 = plt.subplots(figsize=(7,5))
ax3.bar(cases_per_speed['speed'].astype(str),cases_per_speed['cases'], width = 0.6, color = 'r')
ax3.set_ylim(bottom=0, top=5000)
ax3.set_ylabel('Cases')
ax3.spines['right'].set_visible(False) # plt version?
ax3.spines['top'].set_visible(False)
ax3.set_title('Number of cases w.r.t speed limit from 2005-2017', fontsize=14)
plt.savefig('/Users/Pictures/Cases_wrt_weather.png')
plt.show()
##
weather_map={1:'Fine no high winds', 2:'Raining no high winds',
3:'Snowing no high winds',4:'Fine + high winds',5:'Raining + high winds',
6:'Snowing + high winds',7:'Fog or mist',8:'Other',9:'Unknown'}
cases_per_weather['weather_new']=cases_per_weather['weather'].map(weather_map)

fig4, ax4 = plt.subplots(figsize=(8,8))
ax4.semilogy(cases_per_weather['weather_new'],cases_per_weather['cases'], c='r',label='Weather conditions')
ax4.set_ylim(bottom=0, top=10000)
ax4.set_ylabel('Cases (semilog)', fontsize = 12, fontweight ='bold')
ax4.spines['right'].set_visible(False) # plt version?
ax4.spines['top'].set_visible(False)
ax4.set_title('Number of cases w.r.t weather conditions from 2005-2017', fontsize=14, fontweight = 'bold')
plt.xticks(rotation = 90, fontsize = 12, fontweight = 'bold') # Doesn't work with ax3
plt.savefig('/Users/Pictures/Cases_wrt_speed_limit.png')
plt.show()



# Prediction of accident severity [1: Fatal, 2: Serious, 3: Slight]...
# based on the environmental conditions (road, weather, light)
# Create the regressor matrix X
cols_env = ['road_type', 'speed_limit', 'light_conditions', 
            'weather_conditions', 'road_surface_conditions', 
            'special_conditions_at_site']
X = df1.loc[:, cols_env].values
y = df1['accident_severity'].values # df to array


k = list(np.arange(1,30,1))
cv_accuracy = []
cv_error = []

for i in k:
    model_knn = neighbors.KNeighborsClassifier(i)
    model_accuracy=cross_val_score(model_knn, X, y, cv = 5, scoring='accuracy')  
    #https://scikit-learn.org/stable/modules/model_evaluation.html
    cv_accuracy.append(100 * model_accuracy.mean()) # mean of 5-folds, 100 %
    
max_accuracy = max(cv_accuracy)
k_optimal = k[cv_accuracy.index(max_accuracy)]

figKNN, axKNN = plt.subplots(figsize=(6,6))
axKNN.plot(k, cv_accuracy, label = 'Model accuracy')
axKNN.set_xlabel('Neighbors', fontsize='large', fontweight='bold')
axKNN.set_ylabel('Model accuracy (%)', fontsize='large')
axKNN.set_title('Prediction of accident severity using KNN and k-fold CV', fontsize='large', fontweight='bold')
axKNN.scatter(k_optimal, max_accuracy, c = 'r', label = 'Highest accuracy')
axKNN.legend(loc = 'center right')
axKNN.spines['right'].set_visible(False) 
axKNN.spines['top'].set_visible(False)
axKNN.tick_params(axis = 'both', labelsize = 12, fontweight='bold' )
axKNN.set_ylim(0,100)
plt.text(k_optimal, max_accuracy,str(round(max_accuracy, 1)),fontsize=12,fontweight='bold',
                    ha='left',va='bottom',color='black',
                    bbox=dict(facecolor='w', alpha=0.2))
plt.savefig('/Users/Pictures/KNN_kfoldCV.png')
plt.show()
