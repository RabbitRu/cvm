#Во всех метриках А оригинал, B сгенерирован
#Метрики считают единицей длины один план,
#точнее будет учитывать продолжительность каждого плана в кадрах

def _planLength(division, index):
	return division[index][1] - division[index][0]

def _planIntersection(divA, indexA, divB, indexB):
	return max(
		min(divA[indexA][1], divB[indexB][1]) - max(divA[indexA][0],
		divB[indexB][0]), 0)

def _puritySubfunc(divA, divB, T):
	NA = len(divA)
	NB = len(divB)
	leftSum = 0
	rightSum = 0
	result = 0
	for i in range(0, NA):
		rsi = _planLength(divA, i)
		summator = 0
		for j in range (0, NB):
			rsij = _planIntersection(divA, i, divB, j)
			summator = summator + (rsij * rsij) / (rsi * rsi)
		result += rsi * summator / T
	return result

#Метрика Purity, идеал 1
def metricPurity(divA, divB):
	if(divB[-1][1] != divA[-1][1]):
		print("Такого быть не должно, количество кадров должно совпадать")
	totalLength = divB[-1][1]
	leftPart = _puritySubfunc(divA, divB, totalLength)
	rightPart = _puritySubfunc(divB, divA, totalLength)
	return leftPart * rightPart





def _findOverlappings(division, scene):
	leftOverlap = 0
	rightOverlap = 0 
	for i in range(0, len(division)):
		if(scene[0] < division[i][0] and division[i][0] < scene[1]):
			leftOverlap = division[i][0] - scene[0]
		if(scene[0] < division[i][1] and division[i][1] < scene[1]):
			rightOverlap = scene[1] - division[i][1]
	# здесь можно добавить замер времени
	totalOverlap = leftOverlap + rightOverlap
	return totalOverlap

#Метрика Overflow, идеал 0
def metricOverflow(divA, divB):
	summator = 0
	for i in range(0, len(divB)):
		summator += _findOverlappings(divA, divB[i])
	return summator / divB[-1][1]



def _findLagrestOverlappingScene(division, scene):
	maxIntersec = 0
	for i in range(0, len(division)):
		intersection = 0
		if not (division[i][1] < scene[0] or division[i][0] > scene[1]):
			if(division[i][1] < scene[1]):
				# здесь можно добавить замер времени
				intersection = scene[1] - division[i][1]
			else:
				# здесь можно добавить замер времени
				intersection = min(scene[1] - scene[0], scene[1] - division[i][0])
		if(intersection > maxIntersec):
			maxIntersec = intersection
	if(maxIntersec == 0):
		print("Для каждой сцены должно быть пересечение хоть в один план" + str(scene))
	return maxIntersec 

#Метрика Coverage, идеал 1
def metricCoverage(divA, divB):
	summator = 0
	for i in range(0,len(divA)):
		summator += _findLagrestOverlappingScene(
			divB,
			divA[i]) / (divA[i][1] - divA[i][0])
	return summator / len(divA)

#F-мера
def metricFCO(coverage, overflow):
	return (2 * coverage * overflow) / (coverage + overflow)

def metricFCOP(coverage, overflow, purity):
	return (3 * coverage * overflow * purity) / (coverage + overflow + purity)

def getMetrics(origDivision, ourDivision):
	purity = metricPurity(origDivision, ourDivision)
	coverage = metricCoverage(origDivision, ourDivision)
	overflow = metricOverflow(origDivision, ourDivision)
	fmco = metricFCO(coverage, overflow)
	fmcop = metricFCOP(coverage, overflow, purity)
	allMetrics = []
	allMetrics.append('Purity: ' + str(purity))
	allMetrics.append('Coverage: ' + str(coverage))
	allMetrics.append('Overflow: ' + str(overflow))
	allMetrics.append('F-m CO: ' + str(fmco))
	allMetrics.append('F-m COP: ' + str(fmcop))
	return allMetrics











































































