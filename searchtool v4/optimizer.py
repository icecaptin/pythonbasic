from setup import Setup


class HillClimbing:
    def __init__(self):
        Setup.__init__(self)  # Setup 클래스 초기화
        self._pType = 0  # 문제 유형
        self._limitStuck = 100  # FirstChoice 알고리즘에서 사용되는 최대 반복 횟수

        self._numExp = 0
        self._numRestart = 0
    
    def getNumExp(self):
        return self._numExp
    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)

        self._pType = parameters['pType']  # 문제 유형 설정
        self._limitStuck = parameters['limitStuck']
        self._numExp = parameters['numExp']
        self._numRestart = parameters['numRestart']


    def run(self):
        pass

    def randomRestart(self, p):
        self.run(p)
        bestSolution = p.getSolution()
        bestMinnum = p.getValue()
        numEval = p.getNumEval()

        for i in range(1, self._numRestart):
            self.run(p)
            newSolution = p.getSolution()
            newMinnum = p.getValue()
            numEval += p.getNumEval()
            if newMinnum < bestMinnum:
                bestMinnum = newMinnum
                bestSolution = newSolution
        p.storeResult(bestSolution, bestMinnum)


    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutation step size: ", self._delta)  # Numeric 문제에서 사용되는 돌연변이 크기 출력
    
    def displayNumExp(self):
        print()
        print("Number of experiments: ", self._numExp)


class SteepestAscent(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 초기 해 생성
        valueC = p.evaluate(current)  # 초기 해의 평가 값
        while True:
            neighbors = p.mutants(current)  # 현재 해의 이웃 해들 생성
            successor, valueS = self.bestOf(neighbors, p)  # 이웃 해들 중 최적 해 선택
            if valueS >= valueC:  # 현재 해보다 좋은 해가 없으면 종료
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)  # 최적 해와 평가 값 저장

    def bestOf(self, neighbors, p):
        best = neighbors[0]  # 최적 해
        bestValue = p.evaluate(best)  # 최적 해의 평가 값

        for i in range(1, len(neighbors)):
            newValue = p.evaluate(neighbors[i])
            if newValue < bestValue:  # 더 좋은 해가 발견되면 갱신
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue

    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")  # 알고리즘 설정 출력
        HillClimbing.displaySetting(self)  # 부모 클래스의 displaySetting 메서드 호출


class FirstChoice(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 초기 해 생성
        valueC = p.evaluate(current)  # 초기 해의 평가 값
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)  # 현재 해의 랜덤한 돌연변이 생성
            valueS = p.evaluate(successor)  # 돌연변이의 평가 값
            if valueS < valueC:  # 돌연변이가 더 좋은 해이면 갱신
                current = successor
                valueC = valueS
                i = 0  # 반복 횟수 초기화
            else:
                i += 1
        p.storeResult(current, valueC)  # 최적 해와 평가 값 저장

    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")  # 알고리즘 설정 출력
        HillClimbing.displaySetting(self)  # 부모 클래스의 displaySetting 메서드 호출
        print(
            "Max evaluations with no improvement: {0:,} iterations".format(
                self._limitStuck
            )
        )  # 최대 반복 횟수 출력


class GradientDescent(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 초기 해 생성
        valueC = p.evaluate(current)  # 초기 해의 평가 값
        while True:
            successor = p.takeStep(current, valueC)  # 현재 해로부터 다음 해 생성
            valueS = p.evaluate(successor)  # 다음 해의 평가 값
            if valueS >= valueC:  # 현재 해보다 좋은 해가 없으면 종료
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)  # 최적 해와 평가 값 저장

    def takeStep(self, current, i, d):
        curCopy = current[:]
        domain = self._domain
        l = domain[1][i]
        u = domain[2][i]
        if l <= (curCopy[i] + d) <= u:  # 도메인 내에서 이동 가능한 범위인 경우 이동
            curCopy[i] += d
        return curCopy

    def displaySetting(self):
        print()
        print("Search algorithm: Gradient Descent Hill Climbing")  # 알고리즘 설정 출력
        print()
        print("Update rate: ", self._alpha)  # 업데이트 비율 출력
        print("Increment for calculating derivatives: ", self._dx)  # 도함수 계산을 위한 증분 출력
