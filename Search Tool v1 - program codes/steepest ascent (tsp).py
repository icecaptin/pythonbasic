import random
import math

NumEval = 0  # Total number of evaluations


def main():
    # Create an instance of TSP
    p = createProblem()  # 'p': (numCities, locations, table)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, "r")
    # First line is number of cities
    numCities = int(infile.readline())
    locations = []
    line = infile.readline()  # The rest of the lines are locations
    while line != "":
        locations.append(eval(line))  # Make a tuple and append
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)
    return numCities, locations, table


def calcDistanceTable(numCities, locations):
    table = [[0] * numCities for _ in range(numCities)]  # 2차원 리스트 초기화

    for i in range(numCities):
        for j in range(i+1, numCities):  # 대칭 행렬이므로 절반만 계산
            x1, y1 = locations[i]  # 첫 번째 도시의 위치
            x2, y2 = locations[j]  # 두 번째 도시의 위치
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # 유클리드 거리 계산
            table[i][j] = distance  # 대칭 행렬에 거리 저장
            table[j][i] = distance  # 대칭 행렬이므로 반대쪽도 저장

    return table



def steepestAscent(p):
    current = randomInit(p)  # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def randomInit(p):  # Return a random initial tour
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    return init


def evaluate(current, p):
    ## Calculate the tour cost of 'current'
    ## 'p' is a Problem instance
    ## 'current' is a list of city ids
    
    cost = p.evaluate(current)  # Problem 인스턴스의 evaluate 함수 호출하여 목적 함수 값 계산
    return cost



def mutants(current, p):  # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors


def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
        i += 1
        j -= 1
    return curCopy


def bestOf(neighbors, p):
    best = None  # 가장 좋은 이웃을 저장할 변수
    bestValue = float("inf")  # 가장 좋은 이웃의 값(최소 순회 비용). 일단 무한대로 초기화합니다.

    # 주어진 이웃들의 리스트를 순회하면서 각 이웃의 값을 평가합니다.
    for neighbor in neighbors:
        neighborValue = evaluate(
            neighbor, p
        )  # 이웃의 값을 평가합니다. evaluate() 함수로 순회 비용을 계산합니다.

        # 현재까지의 가장 좋은 이웃보다 더 좋은 이웃을 찾으면, 해당 이웃과 그 값을 업데이트합니다.
        if neighborValue < bestValue:
            best = neighbor
            bestValue = neighborValue

    return best, bestValue  # 가장 좋은 이웃과 그 이웃의 값(순회 비용)을 반환합니다.


def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end="")
        if i % 5 == 4:
            print()


def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")


def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)  # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))


def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end="")
        if i % 10 == 9:
            print()


main()
