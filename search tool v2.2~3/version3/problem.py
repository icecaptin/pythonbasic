import math
import random
from setup import Setup


# interface
class Problem:
    def __init__(self):
        Setup.__init__(self)  # Setup 클래스 초기화
        self._solution = []  # 최적해
        self._value = 0  # 최적해의 평가 값
        self._numEval = 0  # 평가 횟수

    def setVariables(self):
        pass

    def randomInit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self):
        pass

    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))


class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)  # Problem 클래스 초기화
        self._expression = ""  # 수식
        self._domain = []  # 변수 도메인

    def getDelta(self):
        return self._delta

    def getAlpha(self):
        return self._alpha

    def getDx(self):
        return self._dx

    def setVariables(self):
        fileName = input("Enter the file name of a function: ")  # 함수 파일명 입력
        infile = open(fileName, "r")
        self._expression = infile.readline().strip()  # 수식 읽어오기
        varNames = []
        low = []
        up = []
        line = infile.readline()
        while line != "":
            data = line.split(",")
            varNames.append(data[0])
            low.append(float(data[1]))
            up.append(float(data[2]))
            line = infile.readline()
        infile.close()
        self._domain = [varNames, low, up]  # 변수 도메인 설정

    def randomInit(self):
        domain = self._domain
        low, up = domain[1], domain[2]
        init = []
        for i in range(len(low)):
            r = random.uniform(low[i], up[i])  # 도메인 내에서 랜덤한 초기 값 생성
            init.append(r)
        return init

    def evaluate(self, current):
        self._numEval += 1
        expr = self._expression
        varNames = self._domain[0]
        for i in range(len(varNames)):
            assignment = varNames[i] + "=" + str(current[i])  # 변수에 값 할당
            exec(assignment)
        return eval(expr)  # 수식 계산 결과 반환

    def mutants(self, current):
        neighbors = []
        for i in range(len(current)):
            mutant = self.mutate(current, i, self._delta)  # 돌연변이 생성
            neighbors.append(mutant)
            mutant = self.mutate(current, i, -self._delta)  # 음의 방향 돌연변이 생성
            neighbors.append(mutant)
        return neighbors

    def mutate(self, current, i, d):
        curCopy = current[:]
        domain = self._domain
        l = domain[1][i]
        u = domain[2][i]
        if l <= (curCopy[i] + d) <= u:  # 도메인 내에서 이동 가능한 범위인 경우 이동
            curCopy[i] += d
        return curCopy

    def randomMutant(self, current):
        i = random.randint(0, len(current) - 1)  # 랜덤한 변수 선택
        if random.uniform(0, 1) > 0.5:  # 돌연변이의 방향 결정
            d = self._delta
        else:
            d = -self._delta
        return self.mutate(current, i, d)

    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)  # 수식 출력
        print("Search space:")
        varNames = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(varNames[i] + ": ({}, {})".format(low[i], up[i]))  # 변수 도메인 출력

    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # 최적해 출력
        print("Minimum value: {0:,.3f}".format(self._value))  # 최적해의 평가 값 출력
        Problem.report(self)  # 부모 클래스의 report 메서드 호출

    def coordinate(self):
        c = [round(value, 3) for value in self._solution]  # 최적해의 좌표값을 소수점 3자리로 반올림
        return tuple(c)

    def takeStep(self, x, v):
        grad = self.gradient(x, v)  # 그래디언트 계산
        xCopy = x[:]
        for i in range(len(x)):
            xCopy[i] -= self._alpha * grad[i]  # 새로운 위치로 이동

        if self.isLegal(xCopy):  # 이동한 위치가 도메인 내에 있는지 확인
            return xCopy
        else:
            return x

    def isLegal(self, x):
        domain = self._domain
        low, up = domain[1], domain[2]
        for i in range(len(low)):
            l, u = low[i], up[i]
            if l[i] <= x[i] <= u:
                pass
            else:
                return False
        return True

    def gradient(self, x, v):
        grad = []
        for i in range(len(x)):
            xCopy = x[:]
            xCopy[i] += self._dx
            df = self.evaluate(xCopy) - v
            g = df / self._dx
            grad.append(g)  # 각 변수에 대한 그래디언트 계산
        return grad


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)  # Problem 클래스 초기화
        self._numCities = 0  # 도시 개수
        self._locations = []  # 도시 좌표
        self._distanceTable = []  # 거리 테이블

    def setVariables(self):
        fileName = input("Enter the file name of a TSP: ")  # TSP 파일명 입력
        infile = open(fileName, "r")
        self._numCities = int(infile.readline())  # 도시 개수 읽어오기
        self._locations = []
        line = infile.readline()
        while line != "":
            self._locations.append(eval(line.strip()))  # 도시 좌표 읽어오기
            line = infile.readline()
        infile.close()
        self._distanceTable = self.calcDistanceTable()  # 거리 테이블 계산

    def calcDistanceTable(self):
        table = []
        locations = self._locations
        for i in range(self._numCities):
            row = []
            for j in range(self._numCities):
                dx = locations[i][0] - locations[j][0]  # x 좌표 차이
                dy = locations[i][1] - locations[j][1]  # y 좌표 차이
                d = round(math.sqrt(dx**2 + dy**2), 1)  # 거리 계산 후 반올림
                row.append(d)
            table.append(row)
        return table

    def randomInit(self):
        n = self._numCities
        init = list(range(n))  # 0부터 n-1까지의 순열 생성
        random.shuffle(init)  # 순열 무작위 섞기
        return init

    def evaluate(self, current):
        self._numEval += 1
        n = self._numCities
        table = self._distanceTable
        cost = 0
        for i in range(n - 1):
            locFrom = current[i]
            locTo = current[i + 1]
            cost += table[locFrom][locTo]  # 연결된 도시 사이의 거리 합산
        return cost

    def mutants(self, current):
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:
            i, j = sorted([random.randrange(n) for _ in range(2)])  # 랜덤한 도시 쌍 선택
            if i < j and [i, j] not in triedPairs:  # 중복 방지
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)  # 선택된 도시 사이 역전
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def inversion(self, current, i, j):
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]  # 위치 교환
            i += 1
            j -= 1
        return curCopy

    def randomMutant(self, current):
        while True:
            i, j = sorted(
                [random.randrange(self._numCities) for _ in range(2)]
            )  # 랜덤한 도시 쌍 선택
            if i < j:
                curCopy = self.inversion(current, i, j)  # 선택된 도시 사이 역전
                break
        return curCopy

    def describe(self):
        print()
        print("Number of cities:", self._numCities)
        print("City locations:")
        locations = self._locations
        for i in range(self._numCities):
            print("{:>12}".format(str(locations[i])), end="")  # 도시 좌표 출력
            if i % 5 == 4:
                print()

    def report(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()  # 최적 순서 출력
        print("Minimum tour cost: {0:,}".format(round(self._value)))  # 최적 순서의 평가 값 출력
        Problem.report(self)  # 부모 클래스의 report 메서드 호출

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{:>5}".format(self._solution[i]), end="")  # 10개씩 한 줄에 출력
            if i % 10 == 9:
                print()
