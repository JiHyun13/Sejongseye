import cv2, json, os

def resize_image_and_update_json(image_path, json_path, output_directory, target_size):
    # 이미지 읽기
    print(f"읽는 중: '{image_path}'")  # 현재 읽고 있는 이미지 경로 출력
    if not os.path.exists(image_path):
        print(f"파일 '{image_path}'가 존재하지 않습니다.")
        return
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"이미지 '{image_path}'를 불러오는 데 실패했습니다.")
        return

    original_height, original_width = image.shape[:2]
    target_width, target_height = target_size

    # 비율 계산
    scale = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # 이미지 리사이즈
    resized_image = cv2.resize(image, (new_width, new_height))

    # JSON 파일 읽기
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # RESOLUTION 값 업데이트
    json_data["RESOLUTION"] = f"{new_width}*{new_height}"

    # 바운딩 박스 조정
    for bounding in json_data["Bounding"]:
        x1 = int(bounding["x1"])
        y1 = int(bounding["y1"])
        x2 = int(bounding["x2"])
        y2 = int(bounding["y2"])

        # 비율에 맞게 조정
        bounding["x1"] = int(x1 * scale)
        bounding["y1"] = int(y1 * scale)
        bounding["x2"] = int(x2 * scale)
        bounding["y2"] = int(y2 * scale)

    # 출력 파일 경로 설정
    output_file_name = os.path.basename(image_path)  # 원본 파일 이름 가져오기
    output_image_path = os.path.join(output_directory, output_file_name)  # 출력 디렉터리에 저장

    # 리사이즈된 이미지 저장
    cv2.imwrite(output_image_path, resized_image)

    # 업데이트된 JSON 파일 저장 (덮어쓰기)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"리사이즈된 이미지가 '{output_image_path}'에 저장되었습니다.")
    print(f"업데이트된 JSON 파일이 '{json_path}'에 저장되었습니다.")

# 사용자에게 입력 받기
root_directory = r"D:\project\Sejongseye\YOLOv8\dataset\train\image"
output_directory = r"D:\project\Sejongseye\YOLOv8\dataset\train\converted_image"
json_directory = r"D:\project\Sejongseye\YOLOv8\dataset\train\json\converted_json"

# 리사이즈할 크기 설정
target_size = (640, 640)  # 예: 640x640

error_log = []  # 오류 로그 리스트 초기화

# 폴더 내 모든 하위 디렉터리 탐색
try:
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for file_name in filenames:
            if file_name.lower().endswith('.jpg'):  # 대소문자 구분 없이 .jpg 파일 처리
                image_path = os.path.join(dirpath, file_name)
                
                # JSON 파일 이름 생성
                json_file_name = os.path.splitext(file_name)[0] + '.json'
                json_path = os.path.join(json_directory, json_file_name)  # JSON 파일 경로를 json_directory에서 가져옴

                # JSON 파일이 존재하는 경우에만 작업 수행
                if os.path.exists(json_path):
                    resize_image_and_update_json(image_path, json_path, output_directory, target_size)
                else:
                    print(f"JSON 파일 '{json_path}'가 존재하지 않습니다.")
except Exception as e:
    print(f"폴더를 읽는 데 오류 발생: {e}")
    error_log.append(str(e))  # 오류를 로그에 추가

# 오류가 발생한 파일 목록을 txt 파일로 저장
if error_log:
    with open(os.path.join(root_directory, 'error_log.txt'), 'w', encoding='utf-8') as f:
        for error_file in error_log:
            f.write(error_file + '\n')
    print(f"오류가 발생한 파일 목록이 'error_log.txt'에 저장되었습니다.")

print("모든 파일 처리가 완료되었습니다.")
