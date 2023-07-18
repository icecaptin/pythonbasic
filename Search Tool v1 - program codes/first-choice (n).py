import random
import math
DELTA = 0.01   # 돌연변이 크기
LIMIT_STUCK = 100  # 개선이 없이 지속되는 최대 평가 횟수
NumEval = 0  # 총 평가 횟수


def main():
    # 숫자 최적화 문제의 인스턴스 생성
    p = createProblem()  # 'p': (식, 도메인)
    # 탐색 알고리즘 호출
    solution, minimum = firstChoice(p)
    # 문제와 알고리즘 설정 표시
    describeProblem(p)
    displaySetting()
    # 결과 보고
    displayResult(solution, minimum)


def createProblem():
    fileName = input("Enter the file name of a problem: ")
    infile = open(fileName, 'r')
    # Read the expression from the file
    expression = infile.readline().strip()
    # Read the domain from the file
    varNames = []
    low = []
    up = []
    line = infile.readline()
    while line != '':
        name, l, u = line.strip().split(',')
        varNames.append(name)
        low.append(float(l))
        up.append(float(u))
        line = infile.readline()
    infile.close()
    domain = [varNames, low, up]
    return expression, domain



def firstChoice(p):
    current = randomInit(p)  # 'current'는 값들의 리스트입니다.
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0  # 개선이 없는 평가 횟수 초기화
        else:
            i += 1
    return current, valueC


def randomInit(p):
    domain = p[1]  # 도메인: [변수명, 최소값, 최대값]
    low = domain[1]  # 변수들의 최소값 리스트
    up = domain[2]  # 변수들의 최대값 리스트
    init = []  # 초기 지점을 담을 리스트
    for i in range(len(low)):
        init.append(random.uniform(low[i], up[i]))  # 각 변수 범위에서 무작위로 선택
    return init



def evaluate(current, p):
    # 'p'에 있는 식에 'current'의 값을 할당한 후 식을 평가합니다.
    global NumEval

    NumEval += 1
    expr = p[0]  # p[0]은 함수 식입니다.
    varNames = p[1][0]  # p[1]은 도메인: [변수명, 최소값, 최대값]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)


def randomMutant(current, p):
    n = len(current)  # 변수의 개수
    i = random.randint(0, n-1)  # 무작위로 위치 선택
    d = random.uniform(-DELTA, DELTA)  # 무작위로 변이 크기 선택
    return mutate(current, i, d, p)



def mutate(current, i, d, p):
    # i번째 값이 범위 내에 있다면 'current'의 i번째를 돌연변이 크기 d만큼 변이시킵니다.
    curCopy = current[:]
    domain = p[1]  # [변수명, 최소값, 최대값]
    l = domain[1][i]  # i번째 변수의 하한값
    u = domain[2][i]  # i번째 변수의 상한값
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy


def describeProblem(p):
    print()
    print("목적 함수:")
    print(p[0])  # 식
    print("탐색 공간:")
    varNames = p[1][0]  # p[1]은 도메인: [변수명, 최소값, 최대값]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i]))


def displaySetting():
    print()
    print("탐색 알고리즘: 첫 번째 선택 힐 클라이밍")
    print()
    print("돌연변이 크기:", DELTA)


def displayResult(solution, minimum):
    print()
    print("찾은 해:")
    print(coordinate(solution))  # 리스트를 튜플로 변환
    print("최소값: {0:,.3f}".format(minimum))
    print()
    print("총 평가 횟수: {0:,}".format(NumEval))


def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # 리스트를 튜플로 변환


main()
