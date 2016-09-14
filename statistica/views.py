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
        'f_i',
        'F_i',
        'f_i\\over N',
        'F_i\\over N',
        'm_i',
        'm_i*f_i',
        'm_i^2*f_i',
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
    max_fi = max([i[1] for i in data])
    mode = []
    Q1_st = int((N+1)/4)
    Q1_nd = int(Q1_st + 1)
    Q3_st = int((N)/4*3)
    Q3_nd = int(Q3_st + 1)
    for j,i in enumerate(data):
        if (float(N/2)) < i[2]:
            LM = data[j][0][0]
            M = j
        elif i[2] <= (float(N/2)) <= data[j+1][2]:
            LM = data[j+1][0][0]
            M = j + 1
        if 0<= abs(i[1] - max_fi) < 0.00001:
            mode.append(i[0])
        
        

    # st_observation = L_st + (j_st-1.0/2)*(U_st-L_st)/f_st
    # nd_observation = L_nd + (j_nd-1.0/2)*(U_nd-L_nd)/f_nd
    # Q1 = st_observation + ((N+1)%4)/4*(nd_observation - st_observation)

    # st_observation3 = L3_st + (j3_st-1.0/2)*(U3_st-L3_st)/f3_st
    # nd_observation3 = L3_nd + (j3_nd-1.0/2)*(U3_nd-L3_nd)/f3_nd
    # Q3 = st_observation3 + ((N)*3%4)/4*(nd_observation3 - st_observation3)

    
            
        
    
    mean = sum([i[6] for i in data])/N


    FM_1 = data[M-1][2]
    fM = data[M][1]
    C = data[0][0][1] - data[0][0][0]
    median = LM + (N/2 - FM_1)/fM*C

    sum_fimisquared = sum([i[7] for i in data])
    mu = sum([i[6] for i in data])/N
    standart_deviation = 0
    variance = 0
    x = mu
    for i in data:
        standart_deviation += (i[1]*((i[5]-mu)**2))
        
    standart_deviation /= N
    variance = (sum_fimisquared - N*(x**2))/(N-1)

    # Q1_1 = (N+1)/4
    # Q3 = input_data[(n+1)*3/4 - 1] + (((n+1)*3%4)/4.0)*(input_data[(n+1)*3/4 ] - input_data[(n+1)*3/4 - 1])
    
    

    return render(request, 'result.html', {
        'data_type':data, 
        'coloumn_name':coloumn_name, 
        'data_range':data_range,
        'N':N,
        'L_M':LM,
        'FM_1':FM_1,
        'fM':fM,
        'C':C,
        'mean':mean,
        'M':M,
        'median':median,
        'mode':mode,
        'standart_deviation':standart_deviation,
        'sum_fimisquared':sum_fimisquared,
        'sqrt_sum_fimisquared':math.sqrt(standart_deviation),
        'variance':variance,
        'x':x,
        'sqrt_variance':math.sqrt(variance),
        # 'st_observation':st_observation3,
        # 'nd_observation':nd_observation3,
        # 'j_st':j3_st,
        # 'L_st':L3_st,
        # 'U_st':U3_st,
        # 'f_st':f3_st,
        # 'Q1':Q3,
        # 'IQR':[Q3 - Q1, Q3, Q1],
        },
        
    )