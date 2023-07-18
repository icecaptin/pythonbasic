from problem import Numeric
import random

LIMIT_STUCK = 100  # Max number of evaluations enduring no improvement

def main():
    # Create an instance of numerical optimization problem
    p = Numeric()
    p.setVariables()
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting()
    # Report results
    p.report()

def firstChoice(p):
    current = p.randomInit()  # 'current' is a list of values
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0  # Reset stuck counter
        else:
            i += 1
    return current, valueC

def randomMutant(current, p):
    # Pick a random locus
    i = random.randint(0, len(current) - 1)
    # Mutate the chosen locus
    if random.uniform(0, 1) > 0.5:
        d = p.getDelta()
    else:
        d = -p.getDelta()
    return p.mutate(current, i, d)

def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())
    print("Max evaluations with no improvement: {0:,} iterations".format(LIMIT_STUCK))

main()
