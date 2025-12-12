import argparse
import os
from omegaconf import OmegaConf

# 우리가 만든 모듈들
from src.utils import Logger, Setting
import src.data as data_module
import src.models as model_module
from src.train import train, test

def main(args):
    # 1. 시드 고정
    Setting.seed_everything(args.seed)

    # 2. 데이터 로드 (동적 호출: context + _data_load)
    # config.yaml에 정의된 datatype (예: 'context')을 가져옴
    datatype = args.model_args[args.model].datatype
    print(f"\n--- [Main] '{datatype}' 타입의 데이터 로딩 함수를 찾습니다 ---")
    
    # getattr로 data.py 안의 함수들(context_data_load 등)을 찾아서 실행
    data_load_fn = getattr(data_module, f'{datatype}_data_load')
    data_split_fn = getattr(data_module, f'{datatype}_data_split')
    data_loader_fn = getattr(data_module, f'{datatype}_data_loader')

    data = data_load_fn(args)
    data = data_split_fn(args, data)
    data = data_loader_fn(args, data)

    # 3. 로그 설정
    setting = Setting()
    logger = Logger(args, setting.get_log_path(args))

    # 4. 모델 초기화 (동적 호출: args.model 이름의 클래스 찾기)
    print(f"\n--- [Main] '{args.model}' 모델을 소환합니다 ---")
    model_class = getattr(model_module, args.model)
    model = model_class(args.model_args[args.model], data).to(args.device)

    # 5. 학습 진행
    if not args.predict:
        model = train(args, model, data, logger, setting)

    # 6. 추론 및 저장
    print(f"\n--- [Main] 결과 저장 중 ---")
    predicts = test(args, model, data, setting)
    
    # 결과가 존재하면 저장 (간단한 출력)
    if predicts:
        print(f"최종 예측 결과(일부): {predicts[:5]} ...")

if __name__ == "__main__":
    # 1. 기본 인자 파싱
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config/config.yaml', help='설정 파일 경로')
    parser.add_argument('--model', type=str, help='모델 이름 (CLI에서 덮어쓰기용)')
    parser.add_argument('--device', type=str, default='cpu', help='장치 설정 (cuda/cpu)')
    
    # parse_known_args를 써서 모르는 인자는 무시(유연성)
    args, _ = parser.parse_known_args()

    # 2. Config 불러오기 및 병합 (CLI > YAML)
    # 파일이 없으면 빈 설정 생성
    if os.path.exists(args.config):
        config_yaml = OmegaConf.load(args.config)
    else:
        print("[Warning] 설정 파일이 없습니다. 기본값으로 진행합니다.")
        config_yaml = OmegaConf.create()

    config_cli = OmegaConf.create(vars(args))
    
    # CLI에서 입력된 값(None이 아닌 것)만 덮어쓰기
    for key in config_cli.keys():
        if config_cli[key] is not None:
            config_yaml[key] = config_cli[key]

    # 3. 메인 실행
    main(config_yaml)