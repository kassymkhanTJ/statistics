import numpy
import math
from collections import Counter
from django.shortcuts import render



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
    mi_squared: 8
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
        'm_i^2',
    ]
    
    # MAIN CONTAINER OF ALL DATA
    data = []
    data_reversed = {}
    # IN DATA
    input_data = request.POST['data'].strip().split(" ")
    n = len(input_data)
    # FREQUENCY COUNT
    N = 0
    
    for i in xrange(n):
        a = input_data[i].split("-")
        data.append([])
        # DATA RANGES
        data[i].append([float(a[0]),float(a[1])])
        # DATA FREQUENCY
        data[i].append(float(a[2]))
        # TOTAL FREQUENCY
        N += float(a[2])

    for i in xrange(n):
        if i==0:
            # FI
            data[i].append(data[i][1])
        else:    
            data[i].append(data[i-1][2] + data[i][1])
        # fi/N
        data[i].append(data[i][1]/float(N))
        # FI/N
        data[i].append(data[i][2]/float(N))
        # MI
        data[i].append(data[i][0][0] + (data[i][0][1] - data[i][0][0])/2)
        # MI*fi
        data[i].append(data[i][5] * data[i][1])
        # MI*fi**2
        data[i].append(data[i][5]**2 * data[i][1])
        # MI**2
        data[i].append(data[i][5]**2)
    
    # MAX fi
    max_fi = max([i[1] for i in data])
    # MODE
    mode = []

    # FIND LM AND M
    for j,i in enumerate(data):
        if i[2] <= (float(N/2)) <= data[j+1][2]:
            LM = data[j+1][0][0]
            M = j + 1
        # FIND MODE
        if 0<= abs(i[1] - max_fi) < 0.00001:
            mode.append(i[0])

    # Q1
    Q1_1 = int((N+1)/4)
    Q1_2 = Q1_1 + 1
    rest1 = (N+1)%4
    # Q3
    Q3_1 = int((N+1)*3/4)
    Q3_2 = Q3_1 + 1
    rest2 = (N+1)*3%4
    # Q1
    for j, i in enumerate(data):
        if Q1_1 <= i[2]:
            if j == 0:
                j11 = Q1_1    
            else:
                j11 = Q1_1 - data[j-1][2]
            L11 = i[0][0]
            U11 = i[0][1]
            f11 = i[1]
            break
        if j == (n-1):
            j11 = Q1_1 - data[j-1][2]
            L11 = i[0][0]
            U11 = i[0][1]
            f11 = i[1]
    for j, i in enumerate(data):
        if Q1_2 <= i[2]:
            if j == 0:
                j12 = Q1_2    
            else:
                j12 = Q1_2 - data[j-1][2]
            L12 = i[0][0]
            U12 = i[0][1]
            f12 = i[1]
            break
        if j == (n-1):
            j12 = Q1_2 - data[j-1][2]
            L12 = i[0][0]
            U12 = i[0][1]
            f12 = i[1]
    # Q3
    for j, i in enumerate(data):
        if Q3_1 <= i[2]:
            if j == 0:
                j31 = Q3_1    
            else:
                j31 = Q3_1 - data[j-1][2]
            L31 = i[0][0]
            U31 = i[0][1]
            f31 = i[1]
            break
        if j == (n-1):
            j31 = Q3_1 - data[j-1][2]
            L31 = i[0][0]
            U31 = i[0][1]
            f31 = i[1]

    
    for j, i in enumerate(data):
        if Q3_2 <= i[2]:
            if j == 0:
                j32 = Q3_2    
            else:
                j32 = Q3_2 - data[j-1][2]
            L32 = i[0][0]
            U32 = i[0][1]
            f32 = i[1]
            break
        if j == (n-1):
            j32 = Q3_2 - data[j-1][2]
            L32 = i[0][0]
            U32 = i[0][1]
            f32 = i[1]
    
    Q1_1_fin = L11 + (j11-1/2.0) *(U11-L11)/f11
    Q1_2_fin = L12 + (j12-1/2.0) *(U12-L12)/f12
    Q1 = Q1_1_fin + rest1/4*(Q1_2_fin - Q1_1_fin)

    Q3_1_fin = L31 + (j31-1/2.0) *(U31-L31)/f31
    Q3_2_fin = L32 + (j32-1/2.0) *(U32-L32)/f32
    Q3 = Q3_1_fin + rest2/4*(Q3_2_fin - Q3_1_fin)
        
    
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
    
    

    return render(request, 'result.html', {
        'data_type':data, 
        'coloumn_name':coloumn_name, 
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
        'Q1_1':[Q1_1, j11, f11, L11, U11, Q1_1_fin, rest1],
        'Q1_2':[Q1_2, j12, f12, L12, U12, Q1_2_fin,],
        'Q3_1':[Q3_1, j31, f31, L31, U31, Q3_1_fin, rest2],
        'Q3_2':[Q3_2, j32, f32, L32, U32, Q3_2_fin,],
        'Q1':Q1,
        'Q3':Q3,
        'IQR':Q3 - Q1,
        
        },
        
    )