import asyncio
import json
import base64
import websockets
import cv2


async def notify_server(websocket, message):
    json_string = json.dumps(message)
    await websocket.send(json_string)


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


async def face_tracking():
    uri = "ws://localhost:8765"
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        async with websockets.connect(uri) as websocket:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Get the angle of the face
            angle = get_face_angle(gray, face_cascade)
            print("angle:", angle)

            if angle is not None:
                await notify_server(websocket, {"type": "face_angle", "data": angle})

            # Display the resulting frame
            cv2.imshow("frame", gray)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


async def main():
    while True:
        await face_tracking()


if __name__ == "__main__":
    asyncio.run(main())
