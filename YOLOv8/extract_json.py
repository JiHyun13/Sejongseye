import json
import os

def filter_json(file_path):
    # JSON 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # 필요한 데이터 추출
    filtered_data = {
        "FILE NAME": json_data["FILE NAME"],
        "DATE": json_data["DATE"],
        "GPS": json_data["GPS"],
        "ID CODE": json_data["ID CODE"],
        "RESOLUTION": json_data["RESOLUTION"],
        "BoundingCount": json_data["BoundingCount"],
        "Bounding": []
    }

    # Bounding에서 필요한 값만 추출
    for bounding in json_data["Bounding"]:
        filtered_bounding = {
            "CLASS": bounding["CLASS"],
            "DETAILS": bounding["DETAILS"],
            "x1": bounding["x1"],
            "x2": bounding["x2"],
            "y1": bounding["y1"],
            "y2": bounding["y2"]
        }
        filtered_data["Bounding"].append(filtered_bounding)

    # 같은 파일에 덮어쓰기
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"필터링된 내용이 '{file_path}'에 저장되었습니다.")


# 사용자에게 파일 경로 입력 받기
data_path = input("원본 JSON 파일의 경로를 입력하세요: ")

# 폴더 내 json 파일 처리
file_list = os.listdir(data_path)

for file_name in file_list:
    if file_name.endswith('.Json'):
        file_path = os.path.join(data_path, file_name)
        filter_json(file_path)
