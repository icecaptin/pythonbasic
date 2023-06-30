import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

# 데이터 로드
data = pd.read_csv('boston_house_price.csv', encoding='utf-8', skiprows=[0])  # 첫 번째 행을 건너뜁니다.

# 데이터셋 정보 출력
print(data.head())

# 열 이름 설정
column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
data.columns = column_names

# 특성과 타겟 데이터 분리
features = data.drop('MEDV', axis=1)
targets = data['MEDV']

# 데이터 정규화
scaler = StandardScaler()
features = scaler.fit_transform(features)

# 훈련 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# 모델 구성
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 훈련
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)

# 테스트 데이터 예측
predictions = model.predict(X_test)

# 예측 결과 출력
for i in range(len(predictions)):
    print('실제 가격: {:.2f}, 예측 가격: {:.2f}'.format(y_test.iloc[i], predictions[i][0]))
