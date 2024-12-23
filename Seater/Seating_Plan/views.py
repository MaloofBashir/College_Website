from django.shortcuts import render
from .seating import getting_all_subs,dictionary_of_subjects
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
import os
from .excel_export import excel_export
from datetime import datetime




# Create your views here.
def index(request):
    return render(request, 'index.html')

def Table_rollno(request):
    context = {}
    date_time=datetime.now()
    context["current_date_time"]=date_time
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']

        # Save the file using FileSystemStorage
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Cache the file URL for later retrieval
        cache.set('uploaded_file_path', file_url, timeout=60*60*24)

        context["file_url"] = file_url
        
        try:
            # Process the file
            getting_all_subs(uploaded_file)
            print(dictionary_of_subjects)
        except Exception:
            error_message = "Error in uploading the file, Please ensure you upload a Pdf-Attendance Sheet from KU"
            context["error"] = error_message

        context["dictionary_of_subjects"] = dictionary_of_subjects
        
        # Render the response and clear the dictionary after rendering
        response = render(request, 'Table_rollno.html', context)

        # Clear dictionary after the response is rendered
        dictionary_of_subjects.clear()
        
        return response
    else:
        # Handle the case where the method is not POST or no file is uploaded
        return render(request, 'Table_rollno.html', context)

def export_excel(request):
    # If you're trying to fetch query parameters from the GET request
    file_url = cache.get('uploaded_file_path')

    if file_url:
        file_path = os.path.join(settings.MEDIA_ROOT, file_url.strip('/'))
        if os.path.exists(file_path):
            # Open the file and return it as a FileResponse for downloading
            with open(file_path, 'rb') as file:
                print(file)
                return excel_export(file)
        # You can send a response with the file URL, or you could return the actual file
        else:
            return HttpResponse("No file found in cache.")
    else:
        return HttpResponse("No file found in cache.")

