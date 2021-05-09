from datetime import timezone,datetime
import requests
import csv
import json

temp_data={}
data=requests.get("https://api.covid19india.org/csv/latest/case_time_series.csv")
if data.status_code==200:
    file_json=open("covid_cases.json",'w+')
    file_csv=open("covid_cases.csv","w+",newline='')
    data=data.content.decode('utf-8')
    
    csv_reader = csv.reader(data.splitlines(), delimiter=',')
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(["Date","Timestamp","Daily Confirmed","Number of cases","Daily Recovered","Total Recovered","Daily Deceased","Total Deceased"])
    
    line_count=1
    for row in csv_reader:
        if line_count!=1:
            timestamp=int(datetime.strptime(row[1], '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
            print("Date:- "+row[1]+" Confirmed:- "+row[3]+" Timestamp:- "+str(timestamp))
            temp_data[str(timestamp)]=int(row[3])

            writer.writerow([str(row[1]),str(timestamp),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7])])
            
            line_count+=1
        else:
            line_count+=1

    file_csv.close()
    file_json.write(json.dumps(temp_data,indent=4))
    file_json.close()
    print("Line Count:- "+str(line_count))
    


