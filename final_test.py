import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def measure(func):
    """
    decorator function
    logging을 이용해 x값, y값, 계산값을 출력할 수 있는 기능을 추가
    """
    def wrapper(args):
        x = args[0]
        y = args[1]
        result = func(x, y)
        logging.info("x=%s, y=%s, result=%s" % (x, y, result))
        return result
    return wrapper

class Evaluator:
    def __init__(self, filename):
        """
        filename에 주어진 경로에서 읽기 전용으로 csv 파일을 읽어서
        각 줄에 있는 수식과 변수 값을 저장

        csv 파일은 수식,x값,y값 으로 구성되어 있음

        ex) equations.txt
        10*x + 2*y,2,5
        0.5*x - 1.8*y,7,3
        """
        with open(filename, 'r') as f:
            self.equations = f.readlines()
        self.equations = [line.strip().split(',') for line in self.equations]

    def solve(self, idx):
        """
        idx 번째 수식을 계산한 값을 반환

        ex)
        solve(1) 은 equations.txt 의 0.5*x - 1.8*y가
        x=7, y=3일 때 값을 계산하여 반환

        solve 내부에는 logging이나 print 사용하지 말 것
        """
        equation, x, y = self.equations[idx]
        x, y = float(x), float(y)  # Convert x and y to float (if needed)
        result = eval(equation, {'x': x, 'y': y})
        return float(result)  # Convert the result back to float

def main():
    evaluator = Evaluator('equations.txt')
    assert np.allclose(evaluator.solve(0), 30)
    assert np.allclose(evaluator.solve(1), -1.9)

main()
