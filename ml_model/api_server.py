from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import numpy as np
import pandas as pd
import os
from typing import Dict

app = FastAPI(
    title="CPS Failure Prediction API",
    description="공정 센서 데이터를 기반으로 기계 고장을 예측하는 API",
    version="1.0.0"
)

# CORS 설정 (C# 앱에서 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 변수로 모델 저장
models = {}
current_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(current_dir, 'models')


class SensorData(BaseModel):
    """센서 데이터 입력 모델"""
    type: str = Field(..., description="제품 타입 (L, M, H)")
    air_temperature: float = Field(..., description="공기 온도 [K]", ge=290, le=310)
    process_temperature: float = Field(..., description="공정 온도 [K]", ge=300, le=315)
    rotational_speed: int = Field(..., description="회전 속도 [rpm]", ge=1000, le=3000)
    torque: float = Field(..., description="토크 [Nm]", ge=0, le=100)
    tool_wear: int = Field(..., description="공구 마모 [min]", ge=0, le=300)

    class Config:
        json_schema_extra = {
            "example": {
                "type": "M",
                "air_temperature": 298.5,
                "process_temperature": 308.7,
                "rotational_speed": 1500,
                "torque": 45.0,
                "tool_wear": 50
            }
        }


class MachineFailurePrediction(BaseModel):
    """기계 고장 예측 결과"""
    prediction: int = Field(..., description="고장 예측 (0: 정상, 1: 고장)")
    probability: float = Field(..., description="고장 확률")


class PredictionResult(BaseModel):
    """전체 예측 결과"""
    machine_failure: MachineFailurePrediction
    failure_types: Dict[str, float] = Field(..., description="각 고장 타입별 확률")

    class Config:
        json_schema_extra = {
            "example": {
                "machine_failure": {
                    "prediction": 1,
                    "probability": 0.87
                },
                "failure_types": {
                    "TWF": 0.12,
                    "HDF": 0.89,
                    "PWF": 0.03,
                    "OSF": 0.15,
                    "RNF": 0.01
                }
            }
        }


@app.on_event("startup")
async def load_models():
    """서버 시작 시 모델 로드"""
    global models

    try:
        print("모델 로딩 중...")

        # 스케일러
        with open(os.path.join(models_dir, 'scaler.pkl'), 'rb') as f:
            models['scaler'] = pickle.load(f)

        # 특성
        with open(os.path.join(models_dir, 'feature_names.pkl'), 'rb') as f:
            models['feature_names'] = pickle.load(f)

        # Machine Failure 모델
        with open(os.path.join(models_dir, 'failure_model.pkl'), 'rb') as f:
            models['failure_model'] = pickle.load(f)

        # Failure Type 모델
        with open(os.path.join(models_dir, 'failure_type_model.pkl'), 'rb') as f:
            models['failure_type_model'] = pickle.load(f)

        print("모델 로딩 완료!!!")
        print(f"특성명: {models['feature_names']}")

    except FileNotFoundError as e:
        print(f"오류: 모델 파일을 찾을 수 없습니다 - {e}")
        print("먼저 train_model.py를 실행하여 모델을 학습시켜주세요.")
        raise
    except Exception as e:
        print(f"모델 로딩 중 오류 발생: {e}")
        raise


def preprocess_input(data: SensorData) -> np.ndarray:
    # Type 원핫 인코딩
    type_L = 1 if data.type == 'L' else 0
    type_M = 1 if data.type == 'M' else 0
    type_H = 1 if data.type == 'H' else 0

    # 특성 순서에 맞게 배열 생성
    # feature_names 순서: numerical features + Type_H, Type_L, Type_M
    features = {
        'Air temperature [K]': data.air_temperature,
        'Process temperature [K]': data.process_temperature,
        'Rotational speed [rpm]': data.rotational_speed,
        'Torque [Nm]': data.torque,
        'Tool wear [min]': data.tool_wear,
        'Type_H': type_H,
        'Type_L': type_L,
        'Type_M': type_M
    }

    # 저장된 특성명 순서대로 값 배열 생성
    feature_values = [features[name] for name in models['feature_names']]

    # DataFrame으로 변환 후 스케일링
    df = pd.DataFrame([feature_values], columns=models['feature_names'])
    scaled = models['scaler'].transform(df)

    return scaled


@app.get("/")
async def root():
    return {
        "message": "CPS Failure Prediction API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    models_loaded = all(key in models for key in ['scaler', 'feature_names', 'failure_model', 'failure_type_model'])
    return {
        "status": "healthy" if models_loaded else "unhealthy",
        "models_loaded": models_loaded
    }


@app.post("/predict", response_model=PredictionResult)
async def predict(data: SensorData):
    
    try:
        # 입력 데이터 전처리
        X = preprocess_input(data)

        # Machine Failure 예측
        failure_pred = models['failure_model'].predict(X)[0]
        failure_proba = models['failure_model'].predict_proba(X)[0]

        # 고장 확률 
        failure_probability = float(failure_proba[1])

        # Failure Type 예측 (확률)
        # MultiOutputClassifier로 각 확률 반환
        failure_type_probas = []
        for estimator in models['failure_type_model'].estimators_:
            proba = estimator.predict_proba(X)[0]

            failure_type_probas.append(proba[1] if len(proba) > 1 else 0.0)

        failure_types = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
        
        # 고장 타입 확률에 전체 고장 확률을 곱해서 조정 make sense한 확률 구하기 위해
        failure_types_dict = {
            failure_type: float(prob * failure_probability)
            for failure_type, prob in zip(failure_types, failure_type_probas)
        }

        result = PredictionResult(
            machine_failure=MachineFailurePrediction(
                prediction=int(failure_pred),
                probability=failure_probability
            ),
            failure_types=failure_types_dict
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"예측 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
