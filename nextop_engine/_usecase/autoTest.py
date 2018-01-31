import statsmodels.tsa.stattools as tsa
import pandas as pd
from pandas import DataFrame
import numpy as np

# checkDataDiscrete

ccode = pd.read_csv("ccode.csv")
# 아래의 값이 이 코드에 있어서 제일 중요한 상수값이다. 이부분에 대해서 이야기 해봐야할듯.
minTermOfAmount = 70;


# 해본결과, 0 데이터는 삭제하는 것이 맞다고 본다. 우선은 급조다.
company = [227645, 230054, 247467, 265812, 269255, 283639]

for i in range (0, 6) :
    a = company[i]
    n = str(a)

    ccodeFor = ccode[n]
    ccodeFor = ccodeFor[ccodeFor.values != 0]

    yValuesOf227645 = []
    yValuesOf227645 = sorted(ccodeFor)

    frequency = pd.value_counts(ccodeFor)
    # print(frequency)
    # print(type(frequency))
    sumOfFrequency = frequency.sum()

    # print(sumOfFrequency)

    maxValueOf227645 = max(yValuesOf227645)
    minValueOf227645 = min(yValuesOf227645)

    # print(maxValueOf227645)
    # print(minValueOf227645)

    totalLength = maxValueOf227645 - minValueOf227645
    expectedMaxN = totalLength / minTermOfAmount

    # print(expectedMaxN)
    line = 0
    sumOfCandidate = 0
    print(frequency)
    for i in frequency:
        if i / sumOfFrequency >= 1 / expectedMaxN:
            sumOfCandidate = sumOfCandidate + i/sumOfFrequency
            # print(i / sumOfFrequency)

            line = line +1
            # print("yes")
    print(n)
    print(sumOfCandidate)
    if sumOfCandidate>= 0.5:
        print("discrete")
    # 알고리즘을 종료한다.
    elif sumOfCandidate>=0.3:
        print("blur")
    # 알고리즘을 다시 돌릴 필요가 있다. 이경우 관찰해본 결과 expectedMaxN이 너무 작게(사실상 최소값이므로) 설정되어 만들어진 결과이다.
    # 아마도 파레트별 expectedMaxN이 따로 있을것이다. 그정도만 넣어줘도 정확도가 급상승할것이 틀림없다.
    # 다시 돌리게 되는데, 이때는 line의 검출값들의 차이중 가장 작은 값을 expectedMaxN으로 주고 해볼 생각이다.
        # 혹은 line간의 최소값들의 평균(288, 256, 400이 있다면, 32, 32, 112의 평균)을 사용해보는건 어떨까.
    # 이떄, 그 값은 70을 넘겨야 할 것이다. 만약 70보다 작은 값이 있다면? boom.
    # 그 구간에 그냥 많이 몰려있고, 아주 작은 주문량을 가진 녀석들이 max값을 가지고 있다고 해석할 수 있다고 본다.
    # 하지만 이것은 어디까지나 여기 6가지 정보를 바탕으로 추측해낸 결과이다.
    # 현재 초안인 만큼 아직 구현을 하지는 않았다.
    else:
        print("continuous")
    # 알고리즘을 종료한다.

    print(line)
    # 더 무엇을 추가하면 좋을까?
    # 처음 생각나는것은 간격, 몇줄이 존재하는지(이건 수정이 필요하다. 현재 70을 절반으로 나눠도 이산성 검출에 문제가 없는가?) 등

# 가동을 위해 임시로 만들어본 부분
# ccodeFor227645 = ccode['227645']
# ccodeFor227645 = ccodeFor227645[ccodeFor227645.values != 0]
#
# yValuesOf227645 = []
# yValuesOf227645 = sorted(ccodeFor227645)
#
# frequency = pd.value_counts(ccodeFor227645)
# print(frequency)
# print(type(frequency))
# sumOfFrequency = frequency.sum()
#
# print(sumOfFrequency)
#
#
# maxValueOf227645 = max(yValuesOf227645)
# minValueOf227645 = min(yValuesOf227645)
#
# # print(maxValueOf227645)
# # print(minValueOf227645)
#
# totalLength = maxValueOf227645 - minValueOf227645
# expectedMaxN = totalLength/minTermOfAmount
#
# # print(expectedMaxN)
# n = 0
# for i in frequency :
#     print(i / sumOfFrequency)
#
#     if i/sumOfFrequency >= 1/expectedMaxN :
#         n=n+1
#         print("yes")
# print(n)


# for i in range (0, 6) :
#     a = company[i]
#     n = str(a)
#     print(n)
#     print("here")
#     print(set(ccode[n]))
#     print(sorted(set(ccode[n])))
#     print(len(set(ccode[n])))
#     print ((len(set(ccode[n])) / len(ccode[n])))



def checkDataDiscrete(dataByCompany, minTerm):
    minTermOfData = minTerm


    return False;

# ADfuller test module
allobject = pd.read_csv("allObject.csv")
allobject.head()
objectcode = [1025, 1041, 1057, 1091, 1111, 1117, 1119, 1127, 1163, 1216, 1242, 1261, 1298, 1355, 1373, 1375, 1376, 1390, 1396, 1627, 1652, 1656, 1692, 1729, 1745, 1754, 1797, 1800, 1815, 1817, 1852, 1853, 1878, 1891]
for i in range(0, len(objectcode)) :
    n = objectcode[i]
    a = str(n)
    # print(n)
    objectnumber = allobject[a]
    series = pd.Series(objectnumber)
    X = series.values
    for i in range(0, len(X)) :
        if (X[i] == 0) :
            X[i] = 1
    pvalue = []
    pvalue.append(tsa.adfuller(X)[1])
    pvalue.append(tsa.adfuller(np.diff(X))[1])
    pvalue.append(tsa.adfuller(np.log(X))[1])
    pvalue.append(tsa.adfuller(np.diff(np.log(X)))[1])
    # print(pvalue)
    minpvalue = min(pvalue)
    minindex = pvalue.index(minpvalue)
    # print(minpvalue, " ", minindex)

# when event
