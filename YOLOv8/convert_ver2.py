import json
import os

def convert_json_to_yolo(json_file_path, output_directory):
    # JSON 파일 읽기
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # YOLO 클래스 ID 매핑 (여기서는 예시로 0을 사용)
    class_mapping = {
        "비닐류": 0,
        "스티로폼류": 1,
        "유리병류": 2,
        "종이류": 3,
        "캔류": 4,
        "페트병류": 5,
        "플라스틱류": 6
    }

    # 이미지 크기
    width, height = map(int, json_data["RESOLUTION"].split('*'))

    # YOLO 형식으로 변환
    yolo_data = []
    for bounding in json_data["Bounding"]:
        class_name = bounding["CLASS"]
        class_id = class_mapping.get(class_name, -1)  # 클래스 ID 찾기
        if class_id == -1:
            continue  # 클래스가 존재하지 않으면 무시

        # 바운딩 박스 좌표
        x1 = int(bounding["x1"])
        y1 = int(bounding["y1"])
        x2 = int(bounding["x2"])
        y2 = int(bounding["y2"])

        # YOLO 형식의 좌표: (x_center, y_center, width, height)
        x_center = (x1 + x2) / 2 / width
        y_center = (y1 + y2) / 2 / height
        box_width = (x2 - x1) / width
        box_height = (y2 - y1) / height

        yolo_data.append(f"{class_id} {x_center} {y_center} {box_width} {box_height}")

    # 확장자 txt로 변경 - class, box 데이터만 일단 사용
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]  # 파일 이름만 추출
    output_filename = os.path.join(output_directory, base_name + '.txt')  # 출력 디렉터리에 저장

    # 파일 저장
    with open(output_filename, 'w', encoding='utf-8') as f:
        for line in yolo_data:
            f.write(line + '\n')

# 사용자에게 상위 폴더 경로 및 출력 폴더 경로 입력 받기
root_directory = "D:/project/Sejongseye/YOLOv8/dataset/train/json/converted_json"
output_directory = "D:/project/Sejongseye/YOLOv8/dataset/train/txt"

# 폴더 내 모든 하위 디렉터리 탐색
try:
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for file_name in filenames:
            if file_name.lower().endswith('.json'):  # 대소문자 구분 없이 .json 또는 .Json 파일 처리
                file_path = os.path.join(dirpath, file_name)
                convert_json_to_yolo(file_path, output_directory)
except Exception as e:
    print(f"폴더를 읽는 데 오류 발생: {e}")

print("모든 파일 처리가 완료되었습니다.")
