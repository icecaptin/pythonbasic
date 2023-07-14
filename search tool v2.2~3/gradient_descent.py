from problem import Numeric
import random

LEARNING_RATE = 0.1  # Learning rate for gradient descent
LIMIT_STUCK = 100  # Max number of iterations enduring no improvement


def main():
    # Create an instance of Numeric problem
    p = Numeric()
    p.setVariables()
    # Call the search algorithm
    solution, minimum = gradientDescent(p)
    p.storeResult(solution, minimum)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)  # Pass 'p' as an argument
    # Report results
    p.report()



def gradientDescent(p):
    current = p.randomInit()  # Initial solution
    valueC = p.evaluate(current)  # Initial value
    i = 0
    while i < LIMIT_STUCK:
        gradient = calculateGradient(p, current)
        successor = updateSolution(current, gradient)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0  # Reset stuck counter
        else:
            i += 1
    return current, valueC


def calculateGradient(p, current):
    gradient = []
    delta = p.getDelta()
    for i in range(len(current)):
        mutant1 = p.mutate(current, i, delta)  # Mutate variable positively
        mutant2 = p.mutate(current, i, -delta)  # Mutate variable negatively
        deltaF = p.evaluate(mutant1) - p.evaluate(
            mutant2
        )  # Calculate change in objective function
        partialDerivative = deltaF / (
            2 * delta
        )  # Approximate partial derivative using central difference
        gradient.append(partialDerivative)
    return gradient


def updateSolution(current, gradient):
    updatedSolution = []
    for i in range(len(current)):
        updatedValue = (
            current[i] - LEARNING_RATE * gradient[i]
        )  # Update variable value using gradient descent
        updatedSolution.append(updatedValue)
    return updatedSolution


def displaySetting(p):
    print()
    print("Search algorithm: Gradient Descent Hill Climbing")
    print()
    print("Step size: ", p.getAlpha())


main()
