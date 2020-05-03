#Student Name: Harwinddranath Muralitheran
#Student_ID: 22254937
#CITS1401 - Project 1
import os

def main():
    file_dict = {} 
    filename = input("Enter file name: ")
    if not os.path.isfile(filename):
        print("File not found.")
        return None
    with open(filename, "r") as handle:
        next(handle)
        for line in handle.readlines():
            array = [line.split(',')[1], line.split(',')[2],line.split(',')[3],line.split(',')[4],line.split(',')[5],line.split(',')[6],line.split(',')[7].replace('\n','')]
            i=0
            while i < len(array):
                if array[i] == '':
                    array[i] = None
                else:
                    array[i] = float(array[i])
                i+=1
            file_dict[line.split(',')[0]] = array
    
    tempDict = {'LogGDP':[0,0],'Social':[0,0],'Healthy':[0,0],'Freedom':[0,0],'Generosity':[0,0],'Confidence':[0,0]}
    tempList = [0,0,0,0,0,0]
    min_list = [float('inf'),float('inf'),float('inf'),float('inf'),float('inf'),float('inf')]
    max_list = [float('-inf'),float('-inf'),float('-inf'),float('-inf'),float('-inf'),float('-inf')]

    for countryKey,rowList in file_dict.items():
        count = 0
        for columnIndex in range(1,7):
            if(rowList[columnIndex]==None):
                continue
            if(rowList[columnIndex]<min_list[count]):
                min_list[count]=rowList[columnIndex]
            if(rowList[columnIndex]>max_list[count]):
                max_list[count]=rowList[columnIndex]
            count+=1
            
    tempDict['LogGDP']=[min_list[0],max_list[0]]
    tempDict['Social']=[min_list[1],max_list[1]]
    tempDict['Healthy']=[min_list[2],max_list[2]]
    tempDict['Freedom']=[min_list[3],max_list[3]]
    tempDict['Generosity']=[min_list[4],max_list[4]]
    tempDict['Confidence']=[min_list[5],max_list[5]]
            
    for countryKey,rowList in file_dict.items():
        count = 0
        for columnIndex in range(1,7):
            if(rowList[columnIndex]==None):
                continue
            rowList[columnIndex]=(rowList[columnIndex]-min_list[count])/(max_list[count]-min_list[count])
            count+=1
    
    metric_dict={}
    
    for countryKey,rowList in file_dict.items():
        minValue = float('inf')
        total = 0
        totalOfInverses = 0
        count = 0
        count2 = 0
        for columnIndex in range(1,7):
            if(rowList[columnIndex]==None):
                continue
            if(rowList[columnIndex]<minValue):
                minValue = rowList[columnIndex]
            total+= rowList[columnIndex]
            count2+=1
            if(rowList[columnIndex]!=0.0):
                totalOfInverses += rowList[columnIndex]**(-1)
                count+=1
        
        meanValue = total/count2
        if(rowList[3] != None and rowList[4] != None):
            medianValue = (rowList[3]+rowList[4])/2
        harmonicValue = (totalOfInverses/count)**(-1)
        
        metric_dict[countryKey]=[minValue,meanValue,medianValue,harmonicValue]
    
    metric_list = ["min", "mean", "median", "harmonic_mean"]
    action_list = ["list", "correlation"]
    metricNumber = -1
    metric = input("Choose a metric to be tested from [min, mean, median, or harmonic_mean]: ")
    if metric not in metric_list:
        print("Please enter a metric within the options available.")
        return
    else:
        print("The metric", metric, "will be used.")
        if (metric == 'min'):
            metricNumber = 0
        elif (metric == 'mean'):
            metricNumber = 1
        elif (metric ==  'median'):
            metricNumber = 2
        elif (metric == 'harmonic_mean'):
            metric_Number = 3
        
    action = input("Choose an action to be performed on the data using the specified metric. The options are 'list' or 'correlation': ")
    if action not in action_list:
        print("Please enter an action within the options available.")
        return 
    else:
        print("The action", action, "will be used.")
        
    if (action == 'list'):
       sorted_results = sorted(metric_dict.items(), key= lambda x:x[1][metricNumber], reverse=True)
       print("Ranked list of countries' happiness scores based on the" + metric + " metric")

       for x in sorted_results:
           print(x[0],round(x[1][metricNumber],4))
        
    elif (action == 'correlation'):
        sorted_metrics = sorted(metric_dict.items(), key= lambda x:x[1][metricNumber], reverse=True)
        sorted_lifeLadder = sorted(file_dict.items(), key= lambda x:x[1][0], reverse=True)

        metricRank = 1
        lifeLadderRank = 1
        ranks_dict = {}
        sumOfSquares = 0
        for x in sorted_metrics:
            ranks_dict[x[0]] = [metricRank,0]
            metricRank += 1
        for x in sorted_lifeLadder:
            ranks_dict.get(x[0])[1] = lifeLadderRank
            lifeLadderRank += 1
        for key,value in ranks_dict.items():
            #print(key, ranks_dict.get(key)[0],'-',ranks_dict.get(key)[1])
            ranks_dict.get(key).append((ranks_dict.get(key)[0]-ranks_dict.get(key)[1])**2)
        for key,value in ranks_dict.items():
            sumOfSquares += value[2]
        
        corr = 1 - (6*((sumOfSquares)/(len(sorted_lifeLadder)*((len(sorted_lifeLadder))**2 -1))))
        print("The correlation coefficient between the study ranking and the ranking using the ", metric, "is :")
        print(round(corr,4))