import csv,json
with open('data.csv','r',newline='') as f:
    data = csv.reader(f)
    output = open('positions.json','w')
    arr = {}
    for i in data:
        arr[i[0]] = {}
        arr[i[0]]['name']=i[1]
        arr[i[0]]['phone']=i[3]
        arr[i[0]]['address']=i[4]
        arr[i[0]]['lng']=i[12]
        arr[i[0]]['lat']=i[13]
    output.write(json.dumps(arr,indent=4,ensure_ascii=False))
    output.close()