from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# from .models import PDF_editor
from .forms import PdfEditorForm

def index(request):
    # dictionary for initial data with
    # field names as keys
    # context ={}

    # add the dictionary during initialization
    # context["dataset"] = HelloModel.objects.all()

    return render(request, "pdf_editor/index.html")

def UploadFile(request):
    if request.method == 'POST':
        form = PdfEditorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('The file is saved')
    else:
        form = PdfEditorForm()
        context = {
            'form':form,
        }
    return render(request, 'pdf_editor/upload.html', context)
