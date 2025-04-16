import base64
import os

import cv2
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from myapp.forms import ImageUploadForm, ImageProcessingForm
from myapp.models import UploadedImage
from myapp.scripts.edgeDetectionV2 import process_uploaded_image
from PIL import Image


def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Image uploaded successfully!")  # Debugging output
            return redirect('home')  # Ensure 'home' is correctly mapped in urls.py
        else:
            print("Form errors:", form.errors)  # Debugging output

    else:
        form = ImageUploadForm()

    images = UploadedImage.objects.all()

    kernel_size = request.session.get('kernel_size', 5)
    wavelet_thresh = request.session.get('wavelet_thresh', 0.07)
    gaussian_coefficient = request.session.get('gaussian_coefficient', 0)
    canny_lower = request.session.get('canny_lower', 100)
    canny_upper = request.session.get('canny_upper', 200)
    line_boldness = request.session.get('line_boldness', 0)
    processed_image = request.session.get('processed_image', None)

    return render(request, 'myapp/home.html', {
        'form': form,
        'images': images,
        'processed_image': processed_image,
        'kernel_size': kernel_size,
        'wavelet_thresh': wavelet_thresh,
        'gaussian_coefficient': gaussian_coefficient,
        'canny_lower': canny_lower,
        'canny_upper': canny_upper,
        'line_boldness': line_boldness,
    })


def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)

    if image.image:
        file_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
        if os.path.isfile(file_path):
            os.remove(file_path)

    image.delete()
    return redirect('home')


def about(request):
    return render(request, 'myapp/about.html')


def process_image(request, image_id):
    image_obj = UploadedImage.objects.get(id=image_id)
    image_path = image_obj.image.path  # Get the absolute path of the image file

    kernel_size = int(request.POST.get('kernel_size', 5))
    wavelet_thresh = float(request.POST.get('wavelet_thresh', .7))
    gaussian_coefficient = int(request.POST.get('gaussian_coefficient', 0))
    canny_lower = int(request.POST.get('canny_lower', 100))
    canny_upper = int(request.POST.get('canny_upper', 200))
    line_boldness = int(request.POST.get('line_boldness', 0))

    request.session['kernel_size'] = kernel_size
    request.session['wavelet_thresh'] = wavelet_thresh
    request.session['gaussian_coefficient'] = gaussian_coefficient
    request.session['canny_lower'] = canny_lower
    request.session['canny_upper'] = canny_upper
    request.session['line_boldness'] = line_boldness

    image = cv2.imread(image_path, 0)  # Read the image with OpenCV (0 for grayscale)
    processed_image = process_uploaded_image(image, kernel_size, wavelet_thresh, gaussian_coefficient, canny_lower, canny_upper, line_boldness)  # Apply your image processing function

    _, buffer = cv2.imencode('.png', processed_image)
    image_bytes = buffer.tobytes()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    request.session['processed_image'] = encoded_image

    # Redirect to the home page
    return redirect('home')
