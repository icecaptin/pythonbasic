import math
import random

# interface
class Problem:
    def __init__(self):
        self._solution = []
        self._value = 0
        self._numEval = 0

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
        Problem.__init__(self)
        self._expression = ''
        self._domain = []
        self._delta = 0.01

    def getDelta(self):
        return self._delta

    def setVariables(self):
        fileName = input("Enter the file name of a function: ")
        infile = open(fileName, 'r')
        self._expression = infile.readline().strip()
        varNames = []
        low = []
        up = []
        line = infile.readline()
        while line != '':
            data = line.split(',')
            varNames.append(data[0])
            low.append(float(data[1]))
            up.append(float(data[2]))
            line = infile.readline()
        infile.close()
        self._domain = [varNames, low, up]

    def randomInit(self):
        domain = self._domain
        low, up = domain[1], domain[2]
        init = []
        for i in range(len(low)):
            r = random.uniform(low[i], up[i])
            init.append(r)
        return init

    def evaluate(self, current):
        self._numEval += 1
        expr = self._expression
        varNames = self._domain[0]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutants(self, current):
        neighbors = []
        for i in range(len(current)):
            mutant = self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i, -self._delta)
            neighbors.append(mutant)
        return neighbors

    def mutate(self, current, i, d):
        curCopy = current[:]
        domain = self._domain
        l = domain[1][i]
        u = domain[2][i]
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def randomMutant(self, current):
        i = random.randint(0, len(current) - 1)
        if random.uniform(0, 1) > 0.5:
            d = self._delta
        else:
            d = -self._delta
        return self.mutate(current, i, d)

    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)
        print("Search space:")
        varNames = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(varNames[i] + ": ({}, {})".format(low[i], up[i]))

    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())
        print("Minimum value: {0:,.3f}".format(self._value))
        Problem.report(self)

    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []
        self._distanceTable = []

    def setVariables(self):
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        self._numCities = int(infile.readline())
        self._locations = []
        line = infile.readline()
        while line != '':
            self._locations.append(eval(line.strip()))
            line = infile.readline()
        infile.close()
        self._distanceTable = self.calcDistanceTable()

    def calcDistanceTable(self):
        table = []
        locations = self._locations
        for i in range(self._numCities):
            row = []
            for j in range(self._numCities):
                dx = locations[i][0] - locations[j][0]
                dy = locations[i][1] - locations[j][1]
                d = round(math.sqrt(dx ** 2 + dy ** 2), 1)
                row.append(d)
            table.append(row)
        return table

    def randomInit(self):
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        self._numEval += 1
        n = self._numCities
        table = self._distanceTable
        cost = 0
        for i in range(n - 1):
            locFrom = current[i]
            locTo = current[i + 1]
            cost += table[locFrom][locTo]
        return cost

    def mutants(self, current):
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def inversion(self, current, i, j):
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def randomMutant(self, current):
        while True:
            i, j = sorted([random.randrange(self._numCities) for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def describe(self):
        print()
        print("Number of cities:", self._numCities)
        print("City locations:")
        locations = self._locations
        for i in range(self._numCities):
            print("{:>12}".format(str(locations[i])), end='')
            if i % 5 == 4:
                print()

    def report(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        Problem.report(self)

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()