import cv2

def make_video_slow(input_video_path, output_video_path):
    # 비디오 캡쳐 객체 생성
    cap = cv2.VideoCapture(input_video_path)

    # 비디오 속성 가져오기
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))

    # 비디오 작성 객체 생성
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # 비디오 재생
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 출력 비디오에 현재 프레임을 두 번 씩 작성 
        out.write(frame)
        out.write(frame)

    # 비디오 역재생을 위해 비디오 캡쳐 객체 초기화
    cap.release()

if __name__ == "__main__":
    input_video_path = './outputvideos/output_reverse.mp4'
    output_video_path = './outputvideos/output_slow.mp4'

    make_video_slow(input_video_path, output_video_path)
