import google.generativeai as genai
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageUploadForm
from .models import Image, DImage
from model.ml_model import detect
from django.core.files.base import ContentFile
import cv2
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import base64

# Create your views here.
# Paths
#  New API Key AIzaSyBRWfmYVvYl3nNmFwoFqjCr4medIecgTZs
#genai.configure(api_key='AIzaSyBE80UKHTx1kjr6gxktbkHBe71mKr3xr2w')
genai.configure(api_key='AIzaSyBRWfmYVvYl3nNmFwoFqjCr4medIecgTZs')

config = "D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\model\yolov3.cfg"
classes = "D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\model\yolov3.txt"
weights = "D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\model\yolov3.weights"


# API
def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Form Saved")
        else:
            form = ImageUploadForm()
            print("Form not valid")

        img = Image.objects.all()
        if len(img) > 0:
            img = img[len(img) - 1]

        return JsonResponse({"link": img.image.path})
    return JsonResponse({"error": "Invalid Request"})


# Django Test
def Detect(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Saved")
        else:
            form = ImageUploadForm()
            print("Form not valid")

        img = Image.objects.all()
        if len(img) > 0:
            img = img[len(img) - 1]

        image_cv2 = detect(img.image.path, config, weights, classes, 1)
        _, buffer = cv2.imencode('.png', image_cv2[0])
        image_bytes = buffer.tobytes()
        image_model = DImage()
        image_model.oimg = img
        image_model.dimg.save('image.png', ContentFile(image_bytes), save=True)

        model = genai.GenerativeModel('gemini-1.5-pro')

        response = model.generate_content("Give us information about" + " ".join(image_cv2[1]))
        formatted_text = response.text

        print(formatted_text)
        print("Detected Img Saved ", image_model.dimg.path)
        return render(request, 'result1.html', context={"image": image_model, "res": formatted_text})
    else:
        form = ImageUploadForm()

    return render(request, 'index1.html', context={'form': form})


def show_logs(request):
    return render(request, "logs.html")


@csrf_exempt
def upload_picture(request):
    if request.method == 'POST':
        # Receive the image data from the client
        image_data = request.POST.get('image')

        # Decode base64 image data
        _, encoded_data = image_data.split(',', 1)
        decoded_data = base64.b64decode(encoded_data)

        # Convert base64 to numpy array
        nparr = np.frombuffer(decoded_data, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Write the image data to a file
        img_path = 'D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\media\\images\\uploaded_picture.jpg'
        cv2.imwrite(img_path, img_np)

        # Process the image
        img_path_det = "D:\\Object Detection Project\\CommonObject\\CommonObject\\ObjectDetector\\media\\dimages\\uploaded_picture.jpg"
        image_cv2 = detect(img_path, config, weights, classes, 1)
        cv2.imwrite(img_path_det, image_cv2[0])

        # Generate content using the processed image
        img_cv2 = list(image_cv2[1])
        for i in range(len(img_cv2)):
            if img_cv2[i].lower() == "person":
                img_cv2[i] = "human"
            elif img_cv2[i].lower() == "mouse":
                img_cv2[i] = "wired mouse"
            elif img_cv2[i].lower() == "apple":
                img_cv2[i] = "apple fruit"

        # model = genai.GenerativeModel('gemini-pro')
        model = genai.GenerativeModel('gemini-1.5-pro')
        if len(img_cv2) != 0:
            response = model.generate_content("Give us information about" + " ".join(img_cv2))
            formatted_text = response.text
        else:
            formatted_text = "Object Not Detected"

        # Define function to format the output

        def format_output(text):
            return text.replace("**", "\n")

        # Format the output
        formatted_output = format_output(formatted_text)

        # Print or use the formatted output
        print(formatted_output)

        # Render the result page, passing the URL of the processed image
        return render(request, 'result2.html',
                      context={"image": '/media/dimages/uploaded_picture.jpg', "res": formatted_output})

    return render(request, 'capture.html')
