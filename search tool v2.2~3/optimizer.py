from setup import Setup


class HillClimbing:
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0
        self._limitStock = 100

    def run(self):
        pass

    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutation step size: ", self._delta)

    def setVariables(self, pType):
        self._pType = pType    


class SteepestAscent(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)
        
    def bestOf(self, neighbors, p):
        best = neighbors[0]  # 'best' is a value list
        bestValue = p.evaluate(best)

        for i in range(1, len(neighbors)):
            newValue = p.evaluate(neighbors[i])
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue
        return best, bestValue
    
    def displaySetting(self): #오버라이딩.
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")              
        HillClimbing.displaySetting(self)


class FirstChoice(HillClimbing):
    def run(self, p):
        current = p.randomInit()   # 'current' is a list of city ids
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStock:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0  # Reset stuck counter
        else:
            i += 1
        p.storeResult(current, valueC)
    
    def displaySetting(self, p):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        HillClimbing.displaySetting(self)
        print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStock))
        


class GradientDescent(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # Initial solution
        valueC = p.evaluate(current)  # Initial value
        while True:
            successor = p.takeStep(current, valueC)
            valueS = p.evaluate(successor)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def takeStep(self, current, i, d): #gradient로 현재 시점에서 좋은걸 가면 되니까 bestof는 필요없다.
        curCopy = current[:]
        domain = self._domain       
        l = domain[1][i]    
        u = domain[2][i]     
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def displaySetting(self):
        print()
        print("Search algorithm: Gradient Descent Hill Climbing")
        print()
        print("Update rate: ", self._alpha)
        print("Increment for caculating derivatives: ", self._dx)
