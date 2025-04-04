import csv
import pandas as pd
import urllib.request
import sys
import codecs

def apiCall():
    try: 
        ResultBytes = urllib.request.urlopen("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/los%20angeles/2010-01-01/2025-03-16?unitGroup=us&elements=datetime%2Ctempmax%2Cdew%2Chumidity%2Cprecip%2Cprecipcover%2Cwindgust%2Cwindspeed%2Csolarradiation&include=days&key=YOUR_API_KEY&contentType=csv")
  
        #Take the data and put it into a csv file
        with open("APICall.csv", "wb") as file:
            file.write(ResultBytes.read()) 

        return "APICall.csv"  #Return the csv file from the api call
        
    except urllib.error.HTTPError  as e:
        print("Error:", e.reason)
        sys.exit()

def calculate_fire_danger(row):
    #Determine fire danger level based on weather conditions.

    #Put the current row data into variables
    tempmax = row["tempmax"]
    dew = row["dew"]
    humidity = row["humidity"]
    precip = row["precip"]
    precipcover = row["precipcover"]
    windgust = row["windgust"]
    windspeed = row["windspeed"]
    solarradiation = row["solarradiation"]
    
    # Fire Danger Score calculation
    T_w = tempmax * 0.3  # Temperature weight
    H_w = ((100 - humidity) + (70 - dew)) * 0.2  # Humidity & Dew Point weight
    P_w = (-precip * 10 - precipcover * 0.3)  # Precipitation weight
    W_w = (windspeed * 0.4 + windgust * 0.6)  # Wind speed weight
    S_w = solarradiation * 0.01  # Solar radiation weight
    
    FDS = (T_w + H_w + P_w + W_w + S_w)
    
    # Apply adjustments
    if precip > 0.1:
        FDS *= 0.7  # Reduce by 30%
    if precipcover > 50:
        FDS *= 0.8  # Reduce by 20%
    if dew > 55:
        FDS *= 0.9  # Reduce by 10%
    
    # Classify Fire Danger Level
    if FDS >= 75:
        return "Extreme"
    elif FDS >= 60:
        return "Very High"
    elif FDS >= 45:
        return "High"
    elif FDS >= 30:
        return "Moderate"
    else:
        return "Low"

def main():
    df = pd.read_csv(apiCall())
    #Fill each empty variables for each day with the average value in the date range except for precipitation which is 0
    df["tempmax"].fillna(df["tempmax"].mean(), inplace=True)  # Fill with average temperature
    df["dew"].fillna(df["dew"].mean(), inplace=True)
    df["humidity"].fillna(df["humidity"].mean(), inplace=True)
    df["precip"].fillna(0, inplace=True)
    df["precipcover"].fillna(0, inplace=True) 
    df["windgust"].fillna(df["windgust"].mean(), inplace=True)
    df["windspeed"].fillna(df["windspeed"].mean(), inplace=True)
    df["solarradiation"].fillna(df["solarradiation"].mean(), inplace=True)
    df["fire_danger_level"] = df.apply(calculate_fire_danger, axis=1)

    # Save the updated dataset
    df.to_csv("NewData.csv", index=False)
    print("New dataset saved as NewData.csv")
    
if __name__ == "__main__":
    main()