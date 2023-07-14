from problem import Tsp
import random

def main():
    # Create an instance of TSP
    p = Tsp()    # 'p': (numCities, locations, table)
    p.setVariables()
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    p.storeResult(solution, minimum)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.report()

def steepestAscent(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def bestOf(neighbors, p):
    best = neighbors[0]
    bestValue = p.evaluate(best)
    for i in range(1, len(neighbors)):
        newValue = p.evaluate(neighbors[i])
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
