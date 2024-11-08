import json

def filter_json(input_file_path, output_file_path):
    # JSON 파일 읽기
    with open(input_file_path, 'r', encoding='utf-8') as f:
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

    # 새로운 JSON 파일로 저장
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"필터링된 JSON 파일이 '{output_file_path}'에 저장되었습니다.")

# 사용자에게 파일 경로 입력 받기
input_file_path = input("원본 JSON 파일의 경로를 입력하세요: ")
output_file_path = input("저장할 필터링된 JSON 파일 이름을 입력하세요 (확장자 포함): ")

# 파일 저장 시 확장자 확인
if not output_file_path.endswith('.json'):
    output_file_path += '.json'

filter_json(input_file_path, output_file_path)
