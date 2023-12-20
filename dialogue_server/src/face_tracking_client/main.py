import asyncio
import json
import base64
import websockets
import cv2
from deepface import DeepFace
import queue
import threading


async def notify_server(message_queue):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await message_queue.get()
            json_string = json.dumps(message)
            await websocket.send(json_string)
            message_queue.task_done()


def get_face_angle(frame, face_cascade):
    # Detect faces
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)
    for x, y, w, h in faces:
        # Calculate the center of the face
        face_center_x = x + w // 2
        # calculate what angle you would need to look at the center of the face depending on the width of the frame
        angle = (face_center_x - frame.shape[1] // 2) / frame.shape[1] * 90
        return angle
    return None


def face_tracking(loop, message_queue):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get the angle of the face
        angle = get_face_angle(gray, face_cascade)
        result = None

        # Detect facial expression
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for x, y, w, h in faces:
            roi_gray = gray[y : y + h, x : x + w]
            roi_color = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2BGR)
            result = DeepFace.analyze(
                roi_color, actions=["emotion"], enforce_detection=False
            )

        dominant_emotion = None
        if result is not None:
            dominant_emotion = result[0]["dominant_emotion"]

        if angle is not None:
            print("angle:", angle, "emotion:", dominant_emotion)
            data = {"angle": angle, "emotion": dominant_emotion}
            message = {"type": "face_data", "data": json.dumps(data)}
            asyncio.run_coroutine_threadsafe(message_queue.put(message), loop)

        # Display the resulting frame
        cv2.imshow("frame", gray)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


async def main():
    message_queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    face_thread = threading.Thread(
        target=face_tracking, args=(loop, message_queue), daemon=True
    )
    face_thread.start()

    notify_task = asyncio.create_task(notify_server(message_queue))
    await notify_task


if __name__ == "__main__":
    asyncio.run(main())
