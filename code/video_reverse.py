import cv2

def play_and_reverse(input_video_path, output_video_path):
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
        
        # 출력 비디오에 현재 프레임 쓰기
        out.write(frame)

    # 비디오 역재생을 위해 비디오 캡쳐 객체 초기화
    cap.release()

    # 역재생을 위한 비디오 캡쳐 객체 생성
    cap = cv2.VideoCapture(input_video_path)

    # 비디오 역재생 및 역재생 비디오 작성
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 출력 비디오에 현재 프레임 쓰기
        frames.append(frame)

    # 비디오 재생이 완료되면 객체 해제
    cap.release()

    # 역재생 비디오 작성
    for frame in reversed(frames):
        out.write(frame)

    # 비디오 작성 객체 해제
    out.release()

if __name__ == "__main__":
    input_video_path = './outputvideos/output (1).mp4'
    output_video_path = './outputvideos/output_reverse.mp4'

    play_and_reverse(input_video_path, output_video_path)
