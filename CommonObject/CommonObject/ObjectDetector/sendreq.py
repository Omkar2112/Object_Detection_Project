import asyncio
import websockets
import cv2
from model.ml_model import detect

# Paths
config = "D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\model\yolov3.cfg"
classes = "D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\model\yolov3.txt"
weights = "D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\model\yolov3.weights"

async def send_message(message):
    uri = "ws://127.0.0.1:8000/ws/detect/"  # Replace with your WebSocket URL
    async with websockets.connect(uri) as websocket:
        message = message  # Message you want to send
        await websocket.send(message)

def read_video(file_path):
    # Open the video file
    cap = cv2.VideoCapture(file_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open the video file.")
        return

    # Read and display frames until the end of the video
    while cap.isOpened():
        ret, frame = cap.read()  # Read a frame from the video

        if ret:  # If frame is read successfully
            temp_img,all_labels = detect(frame,config,weights,classes,1)
            asyncio.get_event_loop().run_until_complete(send_message("Detected : " + " ".join(all_labels)))
            cv2.imshow('Video', temp_img)  # Display the frame

            # Break the loop if 'q' is pressed
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # Release the VideoCapture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Path to the video file
video_path = "D:\\Object Detection Project\\object Video.mp4"
read_video(video_path)
