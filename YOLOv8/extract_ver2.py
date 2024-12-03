import json
import os

def filter_json(file_path, output_directory, error_log):
    try:
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
            class_name = bounding["CLASS"]
            details = bounding["DETAILS"]

            # x1, x2, y1, y2가 주어진 경우
            if "x1" in bounding and "x2" in bounding and "y1" in bounding and "y2" in bounding:
                x1 = bounding["x1"]
                x2 = bounding["x2"]
                y1 = bounding["y1"]
                y2 = bounding["y2"]

            # PolygonPoint가 주어진 경우
            elif "PolygonPoint" in bounding:
                points = []
                
                # PolygonPoint에서 좌표 파싱
                for point in bounding["PolygonPoint"]:
                    # 각 포인트의 값을 추출
                    for value in point.values():
                        x, y = map(int, value.split(','))  # "x,y" 형식으로 되어 있으므로 분리
                        points.append((x, y))

                # x, y 좌표의 최대 및 최소 값 계산
                x_values = [point[0] for point in points]  # x 좌표 리스트
                y_values = [point[1] for point in points]  # y 좌표 리스트
                
                x1 = min(x_values)
                x2 = max(x_values)
                y1 = min(y_values)
                y2 = max(y_values)
                    
            else:
                # x1, x2, y1, y2 또는 PolygonPoint가 없는 경우 처리
                print(f"'{bounding}'에서 x/y 좌표가 없어 건너뜁니다.")
                continue

            # 새로운 바운딩 데이터 생성
            filtered_bounding = {
                "CLASS": class_name,
                "DETAILS": details,
                "x1": x1,
                "x2": x2,
                "y1": y1,
                "y2": y2
            }
            filtered_data["Bounding"].append(filtered_bounding)

        # 출력 파일 경로 설정
        output_file_name = os.path.basename(file_path)  # 원본 파일 이름 가져오기
        output_file_path = os.path.join(output_directory, output_file_name)  # 출력 디렉터리에 저장

        # 같은 파일이름 사용
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"'{file_path}' 처리 중 오류: {e}")
        error_log.append(file_path)  # 오류가 발생한 파일 경로를 로그에 추가


# 사용자에게 상위 폴더 경로 입력 받기
root_directory = input("JSON 파일이 있는 상위 폴더의 경로를 입력하세요: ")
output_directory = input("필터링된 JSON 파일을 저장할 폴더의 경로를 입력하세요: ")

error_log = []  # 오류 로그 리스트 초기화

# 폴더 내 모든 하위 디렉터리 탐색
try:
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for file_name in filenames:
            if file_name.lower().endswith('.json'):  # 대소문자 구분 없이 .json 또는 .Json 파일 처리
                file_path = os.path.join(dirpath, file_name)
                filter_json(file_path, output_directory, error_log)
except Exception as e:
    print(f"폴더를 읽는 데 오류 발생: {e}")

# 오류가 발생한 파일 목록을 txt 파일로 저장
if error_log:
    with open(os.path.join(root_directory, 'error_log.txt'), 'w', encoding='utf-8') as f:
        for error_file in error_log:
            f.write(error_file + '\n')
    print(f"오류가 발생한 파일 목록이 'error_log.txt'에 저장되었습니다.")

print("모든 파일 처리가 완료되었습니다.")
