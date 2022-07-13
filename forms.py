from django import forms
from .models import PdfEditorModel, PdfChooseModifyModel


class PdfEditorForm(forms.ModelForm):
    class Meta:
        model = PdfEditorModel
        fields = ['author', 'title', 'description', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        try:
            filetype = file.content_type
        except:
            raise forms.ValidationError("'%s' is not a file." % file, code='invalid')
        else:
            if not "pdf" in filetype:
                raise forms.ValidationError("File '%s' is not pdf." % file)
        return file


class PdfChooseModifyForm(forms.ModelForm):
    class Meta:
        model = PdfChooseModifyModel
        fields = ['pages_to_duplicate', 'pages_duplicate_copies', 'pages_duplicate_option']

    def clean_pages_duplicate_copies(self):
        copies = self.cleaned_data.get('pages_duplicate_copies', 0)
        if copies < 1:
            raise forms.ValidationError("Incorrect value", code='invalid')
        return copies
