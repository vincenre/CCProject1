from __future__ import print_function

import pandas as pd
from flask import Flask, request, render_template
import json
from flask import abort
from datetime import datetime
import datetime as dt
import time
import requests

app = Flask(__name__)

@app.route("/")
def index():      
    return render_template('index.html')

@app.route('/historical/', methods=["GET","POST"])
def get_alldates():
    global dataset
    
    #Returns all the dates for which weather information is available
    if request.method == "GET":
        weather_list = []
        for i in range(dataset.shape[0]):
            entry = {'DATE':str(dataset['DATE'][i])}
            weather_list.append(entry)
            
        print("Returning %s results" % str(dataset.shape[0]))
        return json.dumps(weather_list)
    
    #Adds a new date, tmax and tmin entry to the dataset
    if request.method == "POST":
        recvData = str(request.get_data(), 'utf-8')
        data = json.loads(recvData)
        d = {'DATE' : int(data["DATE"]), 'TMAX' : data["TMAX"], 'TMIN' : data["TMIN"]}
        print("IN POST INSERT")
        print(d)
        new_df = pd.DataFrame(data=d, columns=['DATE','TMAX','TMIN'], index=[dataset.shape[0]])
        dataset = dataset.append(new_df)
        entry = {'DATE':data["DATE"]}
        print(entry)
        return json.dumps(entry), 201
    return "ERROR"

@app.route('/forecast/<dateYYYYMMDD>', methods=["GET"])
def get_forecast(dateYYYYMMDD):
    global dataset 
    newDate = ""
    #Get forecast for next seven days
    try :
        todaysDate = datetime.strptime(dateYYYYMMDD,'%Y%m%d')
    except ValueError:
        print("Date!!!!")
        return "Please select a Correct Date!"
    forecast_df = pd.DataFrame(columns=['DATE','TMAX','TMIN'])
    new_result = dataset[dataset["DATE"] == int(dateYYYYMMDD)]
    currentYear = dateYYYYMMDD[0:4]
    #print(new_result)
    if new_result.empty:
        year = '2013'
        newDate = year + dateYYYYMMDD[4:8]
        new_result = dataset[dataset["DATE"] == int(newDate)]
        d = {"DATE":str(int(dateYYYYMMDD)),"TMAX":int(new_result["TMAX"]),"TMIN":int(new_result["TMIN"])}  
        todaysDate = datetime.strptime(newDate,'%Y%m%d')
        forecast_df = forecast_df.append(d,ignore_index=True)
        year = 2013
        for i in range(1,7):
            year = 2013
            nextDay = todaysDate + dt.timedelta(days = i)
            #print(nextDay)
            nextdateStr = datetime.strftime(nextDay, '%Y%m%d')
            
            nextDayStr = str(year) + nextdateStr[4:8]
            #print(nextDayStr)
            tempNextDay = nextDayStr
            avg_tmax = 0
            avg_tmin = 0
            for j in range(0,3):
                new_result = dataset[dataset["DATE"] == int(tempNextDay)]
                avg_tmax = avg_tmax + int(new_result["TMAX"])
                avg_tmin = avg_tmin + int(new_result["TMIN"])
                year = year + 1
                tempNextDay = str(year) + tempNextDay[4:8]
                #print(tempNextDay)
            avg_tmax = avg_tmax/3    
            avg_tmin = avg_tmin/3 
            newDateCurrent = currentYear + nextDayStr[4:8]
            d = {'DATE' : newDateCurrent, 'TMAX' : int(avg_tmax)  , 'TMIN' : int(avg_tmin)}
            #print(d)
            forecast_df = forecast_df.append(d,ignore_index=True)
            dataset = dataset.append(d, ignore_index=True)
    else:  
        
        newDate = dateYYYYMMDD
        print(newDate)
        d = {"DATE":str(int(new_result["DATE"])),"TMAX":int(new_result["TMAX"]),"TMIN":int(new_result["TMIN"])}
        todaysDate = datetime.strptime(newDate,'%Y%m%d')
        nextDay =todaysDate
        forecast_df = forecast_df.append(d,ignore_index=True)
        print(forecast_df)
        for i in range(1,7):
            year = 2013
            nextDay = nextDay + dt.timedelta(days = 1)
            print(nextDay)
            nextdateStr = datetime.strftime(nextDay, '%Y%m%d')
            new_result1 = dataset[dataset["DATE"] == int(nextdateStr)]
            if not new_result1.empty:
                d = {"DATE":str(int(nextdateStr)),"TMAX":int(new_result1["TMAX"]),"TMIN":int(new_result1["TMIN"])}  
                forecast_df = forecast_df.append(d,ignore_index=True) 
            else:
                nextDayStr = str(year) + nextdateStr[4:8]
                print("NextDayStr",nextDayStr)
                tempNextDay = nextDayStr
                avg_tmax = 0
                avg_tmin = 0
                for j in range(0,3):
                    new_result2 = dataset[dataset["DATE"] == int(tempNextDay)]
                    avg_tmax = avg_tmax + int(new_result2["TMAX"])
                    avg_tmin = avg_tmin + int(new_result2["TMIN"])
                    year = year + 1
                    tempNextDay = str(year) + tempNextDay[4:8]
                avg_tmax = avg_tmax/3    
                avg_tmin = avg_tmin/3 
                newDateCurrent = currentYear + nextDayStr[4:8]
                d = {'DATE' : newDateCurrent, 'TMAX' : round(float(avg_tmax),2)  , 'TMIN' : round(float(avg_tmin),2)}
                forecast_df = forecast_df.append(d,ignore_index=True)
                d = {'DATE' : int(newDateCurrent), 'TMAX' : round(float(avg_tmax),2)  , 'TMIN' : round(float(avg_tmin),2)}
                dataset = dataset.append(d, ignore_index=True)

    print(forecast_df)        
    return forecast_df.to_json(orient = "records")

@app.route('/historical/<dateYYYYMMDD>', methods=["GET","DELETE"])
def get_details_per_date(dateYYYYMMDD):
    global dataset
    #Get details of a particular date
    time.sleep(5)
    print(dateYYYYMMDD)
    param = int(dateYYYYMMDD)
    if request.method == "GET":
        new_result = dataset[dataset["DATE"] == param]
        print(new_result)
        if new_result.empty:
            return abort(404)
        formatted_result = {"DATE":str(int(new_result["DATE"])),"TMAX":int(new_result["TMAX"]),"TMIN":int(new_result["TMIN"])}
        print(formatted_result)
        return json.dumps(formatted_result)
    #Delete Entry for a particular date
    elif request.method == "DELETE":
        print("In Delete")
        dataset = dataset[dataset["DATE"] != param]
        return "Record for %s deleted" % dateYYYYMMDD
    return "Failure"

@app.route('/fromAPI/<zipcode>', methods=["GET"])
def get_weather_from_API(zipcode):
    r = requests.get("https://api.openweathermap.org/data/2.5/forecast?zip=%d,us&units=imperial&APPID=7f74a98eba389a2d91f680d385909a12" % int(zipcode))
    print(r.text)
    print(r.status_code)
    data = json.loads(r.text)
    oldDate, strTime = data['list'][0]['dt_txt'].split(" ")
    tmax = data['list'][0]['main']['temp_max']
    tmin = data['list'][0]['main']['temp_min']
    forecast_df = pd.DataFrame(columns=['DATE','TMAX','TMIN'])
    for i in range(1, len(data['list'])):
        newDate, strTime = data['list'][i]['dt_txt'].split(" ")
        if newDate == oldDate:
            if data['list'][i]['main']['temp_max'] > tmax:
                tmax = data['list'][i]['main']['temp_max']
            if data['list'][i]['main']['temp_min'] < tmin:
                tmin = data['list'][i]['main']['temp_min']
        else:
            year, month, day = oldDate.split("-")
            dateStr = year+month+day
            print(tmax)
            print(tmin)
            d = {'DATE' : dateStr, 'TMAX' : round(float(tmax),2)  , 'TMIN' : round(float(tmin),2)}
            forecast_df = forecast_df.append(d,ignore_index=True)
            oldDate = newDate
            tmax = data['list'][i]['main']['temp_max']
            tmin = data['list'][i]['main']['temp_min']
            
    year, month, day = oldDate.split("-")
    dateStr = year+month+day
    tmax = tmax
    tmin = tmin
    d = {'DATE' : dateStr, 'TMAX' : round(float(tmax),2)  , 'TMIN' : round(float(tmin),2)}
    forecast_df = forecast_df.append(d,ignore_index=True)
    print(forecast_df)    
    return forecast_df.to_json(orient = "records")
    
if __name__ == '__main__':   
    global dataset
    dataset = pd.read_csv("daily.csv")
    app.run(host="0.0.0.0", port=80)
        




