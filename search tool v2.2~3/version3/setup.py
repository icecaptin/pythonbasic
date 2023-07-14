class Setup:
    def __init__(self):
        self._delta = 0.01  # 돌연변이 생성 시 값의 변화 폭
        self._alpha = 0.01  # Gradient Descent 알고리즘의 업데이트 비율
        self._dx = 10**(-4)  # Gradient Descent 알고리즘의 도함수 근사 계산 시 사용되는 증분값
