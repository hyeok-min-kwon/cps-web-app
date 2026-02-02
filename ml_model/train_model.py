import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle
import os

# 현재 스크립트 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'CPSwithML', 'cps_data.csv')
models_dir = os.path.join(current_dir, 'models')

# 모델 저장 디렉토리 체크
os.makedirs(models_dir, exist_ok=True)

# 이쁘게 띄우기
print("=" * 60)
print("CPS 고장 예측 모델 학습 시작")
print("=" * 60)

# 데이터 로드
print("\n[1] 데이터 로드 중...")
df = pd.read_csv(data_path)
print(f"데이터 크기: {df.shape}")
print(f"\n데이터 샘플:\n{df.head()}")

# 데이터 전처리
print("\n[2] 데이터 전처리 중...")

# BOM 제거 (첫 컬럼명에 포함될 수 있음)
df.columns = df.columns.str.replace('\ufeff', '')

# 특성과 타겟 분리
feature_cols = ['Type', 'Air temperature [K]', 'Process temperature [K]',
                'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
target_failure = 'Machine failure'
target_types = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']

# Type 컬럼 겟더미로 원핫
df_encoded = pd.get_dummies(df[feature_cols], columns=['Type'], prefix='Type')

X = df_encoded
y_failure = df[target_failure]
y_types = df[target_types]

print(f"특성 수: {X.shape[1]}")
print(f"특성명: {list(X.columns)}")
print(f"\n고장 분포:\n{y_failure.value_counts()}")
print(f"\n고장 타입 분포:\n{y_types.sum()}")

# 훈련 테스트 데이터 분할
print("\n[3] 학습/테스트 데이터 분할 (80/20)...")
X_train, X_test, y_failure_train, y_failure_test, y_types_train, y_types_test = train_test_split(
    X, y_failure, y_types, test_size=0.2, random_state=42, stratify=y_failure
)

print(f"학습 데이터: {X_train.shape}")
print(f"테스트 데이터: {X_test.shape}")

# 특성 스케일링
print("\n[4] 특성 스케일링 중...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 스케일러 저장
scaler_path = os.path.join(models_dir, 'scaler.pkl')
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"스케일러 저장 완료: {scaler_path}")

# 특성명 저장 ---> api에 쓰려고
feature_names_path = os.path.join(models_dir, 'feature_names.pkl')
with open(feature_names_path, 'wb') as f:
    pickle.dump(list(X.columns), f)
print(f"특성명 저장 완료: {feature_names_path}")

# 5. 모델 1: Machine Failure 예측
print("\n" + "=" * 60)
print("[5] 모델 1: Machine Failure 예측 (이진 분류)")
print("=" * 60)

failure_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'  # 불균형 데이터 처리하기
)

failure_model.fit(X_train_scaled, y_failure_train)
y_failure_pred = failure_model.predict(X_test_scaled)

# 예측 평가
print("\n*** Machine Failure 모델 평가 ***")
print(f"정확도: {accuracy_score(y_failure_test, y_failure_pred):.4f}")
print(f"\n분류 리포트:\n{classification_report(y_failure_test, y_failure_pred, target_names=['정상', '고장'])}")
print(f"\n혼동 행렬:\n{confusion_matrix(y_failure_test, y_failure_pred)}")

# 특성 중요도
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': failure_model.feature_importances_
}).sort_values('importance', ascending=False)
print(f"\n특성 중요도:\n{feature_importance}")

# 모델 저장
failure_model_path = os.path.join(models_dir, 'failure_model.pkl')
with open(failure_model_path, 'wb') as f:
    pickle.dump(failure_model, f)
print(f"\n모델 저장 완료: {failure_model_path}")

# 모델 2: Failure Type 예측
print("\n" + "=" * 60)
print("[6] 모델 2: Failure Type 예측 (다중 레이블 분류)")
print("=" * 60)

# 고장이 발생한 데이터만 사용
failure_indices_train = y_failure_train == 1
failure_indices_test = y_failure_test == 1

X_train_failures = X_train_scaled[failure_indices_train]
y_types_train_failures = y_types_train[failure_indices_train]
X_test_failures = X_test_scaled[failure_indices_test]
y_types_test_failures = y_types_test[failure_indices_test]

print(f"고장 데이터 - 학습: {X_train_failures.shape}, 테스트: {X_test_failures.shape}")

failure_type_model = MultiOutputClassifier(
    RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
)

failure_type_model.fit(X_train_failures, y_types_train_failures)
y_types_pred = failure_type_model.predict(X_test_failures)

# 평가
print("\n*** Failure Type 모델 평가 ***")
for i, col in enumerate(target_types):
    print(f"\n{col}:")
    print(f"  정확도: {accuracy_score(y_types_test_failures.iloc[:, i], y_types_pred[:, i]):.4f}")
    print(f"  실제 고장 수: {y_types_test_failures.iloc[:, i].sum()}, 예측 고장 수: {y_types_pred[:, i].sum()}")

# 모델 저장
failure_type_model_path = os.path.join(models_dir, 'failure_type_model.pkl')
with open(failure_type_model_path, 'wb') as f:
    pickle.dump(failure_type_model, f)
print(f"\n모델 저장 완료: {failure_type_model_path}")

print("\n" + "=" * 60)
print("학습 완료!")
print("=" * 60)
print(f"\n저장된 파일:")
print(f"  - {scaler_path}")
print(f"  - {feature_names_path}")
print(f"  - {failure_model_path}")
print(f"  - {failure_type_model_path}")
