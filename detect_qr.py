import cv2, requests

camera_id = 0
delay = 1
window_name = 'OpenCV QR Code'

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)

def detection_capture():
    while True:
        ret, frame = cap.read()

        if ret:
            frame = cv2.flip(frame, 1)
            ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
            if ret_qr:
                for value, bounding_box in zip(decoded_info, points):
                    if value:
                        print(value)
                        color = (0, 255, 0)
                        return value
                    else:
                        color = (0, 0, 255)
                    frame = cv2.polylines(frame, [bounding_box.astype(int)], True, color, 5)
            cv2.imshow(window_name, frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cv2.destroyWindow(window_name)

if __name__ == "__main__":
    quit=True
    while quit:
        qr_encoded_value = detection_capture()

        try:
            response = requests.post("http://127.0.0.1:8000/attendance/confirm/", json={"identifier":qr_encoded_value})
            response.raise_for_status()
        except requests.HTTPError:
            pass


