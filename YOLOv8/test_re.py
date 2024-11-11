import cv2
import json
import os

def resize_image_and_update_json(image_path, json_folder, new_size, output_folder):
    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        print("이미지를 읽을 수 없습니다.")
        return
    
    # 원본 이미지 크기
    original_height, original_width = image.shape[:2]
    
    # 비율 계산
    ratio_x = new_size[0] / original_width
    ratio_y = new_size[1] / original_height
    
    # 이미지 리사이즈
    resized_image = cv2.resize(image, new_size)
    
    # 새로운 해상도 문자열 생성
    new_resolution = f"{new_size[0]}*{new_size[1]}"
    
    # JSON 파일 이름 생성
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    json_path = os.path.join(json_folder, f"{base_name}.json")
    
    if not os.path.exists(json_path):
        print("해당 폴더에 JSON 파일이 없습니다.")
        return
    
    # JSON 파일 읽기
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    
    # RESOLUTION 업데이트
    data['RESOLUTION'] = new_resolution
    
    # x1, x2, y1, y2 값 업데이트
    data['x1'] = int(data.get('x1', 0) * ratio_x)
    data['x2'] = int(data.get('x2', 0) * ratio_x)
    data['y1'] = int(data.get('y1', 0) * ratio_y)
    data['y2'] = int(data.get('y2', 0) * ratio_y)
    
    # JSON 파일 저장
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    # 리사이즈된 이미지 저장
    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_image_path, resized_image)
    print(f"이미지와 JSON 파일이 성공적으로 업데이트되었습니다: {output_image_path}, {json_path}")

# 사용 예시
image_path = 'test data/bob/11_X001_C024_1218/11_X001_C024_1218_0.jpg'  # 절대 경로로 이미지 파일 지정
json_folder = 'test data/json'  # JSON 파일이 있는 폴더
new_size = (640, 640)  # 새로운 해상도
output_folder = 'test data/resize img'  # 리사이즈된 이미지를 저장할 폴더

resize_image_and_update_json(image_path, json_folder, new_size, output_folder)
