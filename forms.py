from django import forms
from .models import PdfEditorModel

class PdfEditorForm(forms.ModelForm):
    class Meta:
        model = PdfEditorModel
        fields = ['author', 'title', 'description', 'file']
