from django.shortcuts import (render, redirect, reverse)
from django.contrib import messages
from django.contrib.messages import get_messages
# from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from .forms import PdfEditorForm, PdfChooseModifyForm


def index(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    msg = get_messages(request)
    if msg:
        context['title'] = "File saved"
    else:
        context["title"] = "PDF editor"

    return render(request, "pdf_editor/index.html", context)


def UploadFile(request):
    context = {'title': "Upload PDF file"}
    if request.method == 'POST':
        form = PdfEditorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'The file is saved')
            # return HttpResponse('The file is saved')
            return redirect(reverse('pdf_editor:ChooseModifyFile'))
        else:
            context['form'] = form
    else:
        form = PdfEditorForm()
        context['form'] = form
    return render(request, 'pdf_editor/upload.html', context)


def ChooseModifyFile(request):
    context = {'title': "Choose modify PDF file"}
    if request.method == 'POST':
        form = PdfChooseModifyForm(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'The file start modify')
            return redirect(reverse('pdf_editor:index'))
        else:
            context['form'] = form
    else:
        form = PdfChooseModifyForm()
        context['form'] = form
    return render(request, 'pdf_editor/modify.html', context)
