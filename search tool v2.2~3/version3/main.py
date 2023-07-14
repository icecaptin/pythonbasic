from problem import *
from optimizer import *

def main():
    p, pType = selectProblem() #pType: 1(Numeric) or 2(Tsp)
    alg = selectAlgorithm(pType)
    alg.run(p)
    
    p.describe()
    alg.displaySetting()
    # Report results
    p.report()

def selectProblem():

    print("Select the problem type:")
    print("1. Numeric")
    print("2. Tsp")

    pType = int(input("Enter the number: "))

    if pType == 1:
        p = Numeric() 
    elif pType == 2:
        p = Tsp()
    else:
        print("error")
        raise Exception #예외처리
    
    p.setVariables()
    return p, pType

def selectAlgorithm(pType):
    print()
    print("Select the algorithm: ")
    print(" 1. Steepest Ascent")
    print(" 2. First Choice")
    if(pType == 1):
        print(" 3. Gradient Descent")      

    aType = int(input("Enter the number: "))
    
    optimizers = {1:'SteepestAscent' , 2:'FirstChoice' , 3:'GradientDescent', 4:'Stochastic'}    
    alg = eval(optimizers[aType] + '()') #키값에 따라 value가 나와야. 키는 aType에 다 들어가있다. optimizers[aType] 이것만 하면 string이 된다.
    #그냥 string을 원하는게 아니라 실행하는게 할당되어야... 즉 "SteepestAscent()" 라는 글자가 아니라 SteepestAscent()라는 오브젝트가 되어야하니까.
    alg.setVariables(pType)    
    return alg

main()