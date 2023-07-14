from problem import Tsp
import random

LIMIT_STUCK = 100  # Max number of evaluations enduring no improvement

def main():
    # Create an instance of TSP
    p = Tsp()
    p.setVariables()
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    p.storeResult(solution, minimum)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.report()

def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0  # Reset stuck counter
        else:
            i += 1
    return current, valueC

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print("Max evaluations with no improvement: {0:,} iterations".format(LIMIT_STUCK))

main()
