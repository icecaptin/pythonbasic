from problem import *
from optimizer import *

def main():
    p, pType = selectProblem()  # 문제 선택
    alg = selectAlgorithm(pType)  # 알고리즘 선택
    alg.run(p)  # 알고리즘 실행

    p.describe()  # 문제 설명
    alg.displaySetting()  # 알고리즘 설정 출력
    # 결과 보고
    p.report()

def selectProblem():
    # 문제 유형 선택
    print("문제 유형을 선택하세요:")
    print("1. Numeric")
    print("2. Tsp")
    pType = int(input("숫자를 입력하세요: "))

    if pType == 1:
        p = Numeric()  # Numeric 문제 객체 생성
    elif pType == 2:
        p = Tsp()  # Tsp 문제 객체 생성
    else:
        print("에러")
        raise Exception  # 예외 처리

    p.setVariables()  # 변수 설정
    return p, pType

def selectAlgorithm(pType):
    print()
    print("알고리즘을 선택하세요: ")
    print(" 1. Steepest Ascent")
    print(" 2. First Choice")
    if pType == 1:
        print(" 3. Gradient Descent")

    aType = int(input("숫자를 입력하세요: "))

    # 알고리즘 선택
    optimizers = {1: 'SteepestAscent', 2: 'FirstChoice', 3: 'GradientDescent', 4: 'Stochastic'}
    alg = eval(optimizers[aType] + '()')  # 문자열로 된 알고리즘 이름을 클래스 객체로 변환
    alg.setVariables(pType)  # 변수 설정
    return alg

main()
