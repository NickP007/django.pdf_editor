from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
# from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
# from .models import PDF_editor
from .forms import PdfEditorForm


def index(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    msg = get_messages(request)
    if msg:
        context = {
            'title': "File saved",
        }
    else:
        context["title"] = "PDF editor"

    return render(request, "pdf_editor/index.html", context)


def UploadFile(request):
    if request.method == 'POST':
        form = PdfEditorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'The file is saved')
            # return HttpResponse('The file is saved')
            return redirect('pdf_editor:index')
    else:
        form = PdfEditorForm()
        context = {
            'form': form,
            'title': "Upload PDF file",
        }
    return render(request, 'pdf_editor/upload.html', context)
