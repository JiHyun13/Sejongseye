import json, os

def convert_json_to_yolo(json_file_path):
    # JSON 파일 읽기
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # YOLO 클래스 ID 매핑 (여기서는 예시로 0을 사용)
    class_mapping = {
        "가구류": 0  # 예시: 가구류가 클래스 0에 해당
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
    base_name = os.path.splitext(json_file_path)[0]  # 확장자를 제외한 파일 이름
    output_filename = base_name + '.txt'  # 새로운 파일 이름 (예: 원래이름.txt)
    
    # 파일 저장
    with open(output_filename, 'w', encoding='utf-8') as f:
        for line in yolo_data:
            f.write(line + '\n')

# 사용자에게 상위 폴더 경로 입력 받기
root_directory = input("JSON 파일이 있는 상위 폴더의 경로를 입력하세요: ")

# 폴더 내 모든 하위 디렉터리 탐색
try:
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for file_name in filenames:
            if file_name.lower().endswith('.json'):  # 대소문자 구분 없이 .json 또는 .Json 파일 처리
                file_path = os.path.join(dirpath, file_name)
                convert_json_to_yolo(file_path)
except Exception as e:
    print(f"폴더를 읽는 데 오류 발생: {e}")

print("모든 파일 처리가 완료되었습니다.")
