from django.shortcuts import (render, redirect, reverse)
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponse #, HttpResponseRedirect

# Create your views here.
from .forms import PdfEditorForm, PdfChooseModifyForm


def index(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    try:
        saved_form_id = int(request.session['uploaded_id'])
        download_filename = request.session['download_filename']
    except:
        pass
    else:
        context['download_filename'] = download_filename

    context['title'] = "PDF editor"
    return render(request, "pdf_editor/index.html", context)


def UploadFile(request):
    context = {'title': "Upload PDF file"}
    if request.method == 'POST':
        form = PdfEditorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['uploaded_id'] = str(form.instance.id)
            messages.add_message(request, messages.SUCCESS, 'The file is saved')
            # return HttpResponse('The file is saved')
            return redirect(reverse('pdf_editor:ChooseModifyFile'))
    else:
        form = PdfEditorForm()
    context['form'] = form
    return render(request, 'pdf_editor/upload.html', context)


def ChooseModifyFile(request):
    context = {'title': "Choose modify PDF file"}
    if request.method == 'POST':
        form = PdfChooseModifyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                saved_form_id = int(request.session['uploaded_id'])
            except:
                messages.add_message(request, messages.ERROR, "Unknown error: can't read session variable 'uploaded_id'.")
            else:
                result, new_filename = form.Modify_PDF_file(saved_form_id)
                if result < 0:
                    messages.add_message(request, messages.SUCCESS, 'The file modify is complete. Starting download...')
                    request.session['download_filename'] = new_filename
                else:
                    messages.add_message(request, messages.ERROR, "Unknown error: can't modify PDF file.")
            return redirect(reverse('pdf_editor:index'))
    else:
        form = PdfChooseModifyForm()
    context['form'] = form
    return render(request, 'pdf_editor/modify.html', context)


def DownloadFile(request):
    import os, mimetypes
    #filename = ''
    try:
        saved_form_id = int(request.session.pop('uploaded_id'))
        filename = request.session.pop('download_filename')
    except:
        pass
    else:
        if filename != '':
            path = open(filename, 'rb')
            mime_type, _ = mimetypes.guess_type(filename)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(filename)
            return response
    return redirect(reverse('pdf_editor:index'))
