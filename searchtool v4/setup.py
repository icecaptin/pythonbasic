class Setup:
    def __init__(self):
        self._aType = 0
        self._delta = 0.0  # 돌연변이 생성 시 값의 변화 폭
        self._alpha = 0.0  # Gradient Descent 알고리즘의 업데이트 비율
        self._dx = 0  # Gradient Descent 알고리즘의 도함수 근사 계산 시 사용되는 증분값
    
    def setVariables(self, parameters):
        self._aType = parameters['aType']
        self._delta = parameters['delta']
        self._alpha = parameters['alpha']
        self._dx = parameters['dx']
    
    def getAtype(self):
        return self._aType