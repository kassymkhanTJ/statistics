import numpy
import math
from collections import Counter
from django.shortcuts import render

# Create your views here.
def main(reqest):
    return render(reqest, 'index.html')

def range(request):
    return render(request, 'range.html')

def calculate(request):
    data = {}
    input_data = map(float, request.POST['data'].strip().split(" "))
    input_data.sort()
    n = len(input_data)
    data['mean'] = numpy.mean(input_data)
    data['median'] = numpy.median(input_data)
    histogram = {}
    maximum = 0
    for i in input_data:
        histogram[i] = histogram.get(i, 0) + 1
        maximum = max(histogram.values())
    
    if maximum == 1:
        data['mode'] = None
    else:
        data['mode'] = [item for item in histogram.keys() if histogram[item] == maximum]

    
    data['s_sqared'] = (sum([i*i for i in input_data]) - data['mean']**2*n)/(n-1)
    data['s'] = math.sqrt(data['s_sqared'])

    data['Q1'] = input_data[(n+1)/4 - 1] + (((n+1)%4)/4.0)*(input_data[(n+1)/4 ] - input_data[(n+1)/4 - 1])
    data['Q3'] = input_data[(n+1)*3/4 - 1] + (((n+1)*3%4)/4.0)*(input_data[(n+1)*3/4 ] - input_data[(n+1)*3/4 - 1])
    data['IQR'] = data['Q3'] - data['Q1']
    
    
    return render(request, 'result.html', {'data':data})

def calculate_range(request):
    """
    data_type: 0
    fi: 1
    Fi: 2
    fi_N: 3
    Fi_n: 4
    mi: 5
    miMultfi: 6
    mi_squaredMultfi: 7
    """
    coloumn_name = [
        'Data',
        'fi',
        'Fi',
        'fi/N',
        'Fi/N',
        'mi',
        'mi*fi',
        'mi^2*fi',
    ]
    data = []
    data_reversed = {}
    input_data = request.POST['data'].strip().split(" ")
    n = len(input_data)
    N = 0
    
    for i in xrange(n):
        a = input_data[i].split("-")
        data.append([])
        data[i].append([float(a[0]),float(a[1])])
        data[i].append(float(a[2]))
        N += float(a[2])

    for i in xrange(n):
        if i==0:
            data[i].append(data[i][1])
        else:    
            data[i].append(data[i-1][2] + data[i][1])
        data[i].append(data[i][1]/float(N))
        data[i].append(data[i][2]/float(N))
        data[i].append(data[i][0][0] + (data[i][0][1] - data[i][0][0])/2)
        data[i].append(data[i][5] * data[i][1])
        data[i].append(data[i][5]**2 * data[i][1])

    data_range = {'start':data[0][0][0], 'end':data[-1][0][0]}
     

    
    # for i in xrange(n):
    #     if i==0:
    #         data[i]["Fi"] = data[i]["fi"]
            
    #     else:    
    #         data[i]['Fi'] = data[i-1]['Fi'] + data[i]['fi']
    #     data[i]['fi_N'] = data[i]['fi']/float(N)
    #     data[i]['Fi_N'] = data[i]['Fi']/float(N)
    #     data[i]['mi'] = data[i]['data_type'][0] + (data[i]['data_type'][1] - data[i]['data_type'][0])/2
    #     data[i]['miMultfi'] = data[i]['mi'] * data[i]['fi']
    #     data[i]['mi_squaredMultfi'] = data[i]['mi'] **2 * data[i]['fi']
    # table = []
    # for i in xrange(n):
    #     table.append(data[i])



    return render(request, 'result.html', {'data_type':data, 'coloumn_name':coloumn_name, 'data_range':data_range})