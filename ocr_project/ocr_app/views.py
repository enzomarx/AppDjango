from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import pytesseract
from PIL import Image

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file_path = document.file.path
            text = pytesseract.image_to_string(Image.open(file_path))
            words = text.split()
            return render(request, 'ocr_app/editor.html', {'words': words})
    else:
        form = DocumentForm()
    return render(request, 'ocr_app/upload.html', {'form': form})

def generate_txt(request):
    if request.method == 'POST':
        layout = request.POST.get('layout')
        words = request.POST.getlist('words')
        with open('output.txt', 'w') as f:
            f.write(layout.format(*words))
        return render(request, 'ocr_app/success.html')
    return redirect('upload_document')
