import cv2
from deepface import DeepFace
from django.shortcuts import render
from django.http import StreamingHttpResponse

def analyze_webcam(request):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError('Cannot open webcam.')

    while True:
        ret, frame = cap.read()
        result = DeepFace.analyze(frame, actions=['emotion'])

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,
                    result[0]['dominant_emotion'],
                    (0, 50),
                    font, 3,
                    (0, 0, 255),
                    2,
                    cv2.LINE_4)

        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()
    cv2.destroyAllWindows()

def webcam_view(request):
    return render(request, 'index.html')

def webcam_feed(request):
    return StreamingHttpResponse(analyze_webcam(request), content_type='multipart/x-mixed-replace; boundary=frame')

