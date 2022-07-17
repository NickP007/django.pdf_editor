import re
from django import forms
from PyPDF2 import PdfReader, PdfWriter
from .models import PdfEditorModel, PdfChooseModifyModel


class PdfEditorForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
    )

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
            if "pdf" not in filetype:
                raise forms.ValidationError("File '%s' is not pdf." % file)
        return file
    """
    def tmp_func(self):
        queryset = self.Meta.model._default_manager.get_queryset()
        for set in queryset:
            print(set.get_id)
        field = queryset.model._meta.pk
        print("%s / %s" % (field, self.__class__.__name__))
        print(self.fields)
    """


class PdfChooseModifyForm(forms.ModelForm):
    duplicate_copies = forms.IntegerField(
        label='Number of Copies:', initial=1,
        help_text='Input number between 1 and 1000',
        widget=forms.NumberInput(attrs={'min': 1, 'max': 1000}),
    )
    duplicate_option = forms.ChoiceField(
        label='Duplicate option:',
        help_text='1 1 1, 2 2 2 ... or 1 2 3, 1 2 3 ...',
        widget=forms.Select(),
        choices=PdfChooseModifyModel.PAGE_DUPLICATE_OPTION_CHOISES,
    )

    class Meta:
        model = PdfChooseModifyModel
        fields = ['pages_to_duplicate', 'duplicate_copies', 'duplicate_option']

    def clean_pages_to_duplicate(self):
        pages = self.cleaned_data.get('pages_to_duplicate', '1')
        invalid_symbols = re.findall('[^-,\s\d]', pages)
        if invalid_symbols != []:
            raise forms.ValidationError("Incorrect value. Use digits, coma(','), range separator('-') and space(' ')", code='invalid')
        return pages

    def clean_duplicate_copies(self):
        copies = int(self.cleaned_data.get('duplicate_copies', 0))
        if copies < 1:
            raise forms.ValidationError("Incorrect value", code='invalid')
        return copies

    def Modify_PDF_file(self, form_id):
        def get_filename(path):
            from pathlib import Path
            p = Path(path)
            return p.stem, p.parent

        def get_duplicate_pages_num(pages_count):
            pages_count = int(pages_count)
            dupl_pagesB: bool = [False for i in range(pages_count)]
            pages = self.data.get('pages_to_duplicate')
            pages = re.sub('[^-,\d]', '', pages).split(',')
            for pg in pages:
                r0 = re.split('-', pg)
                if len(r0) == 1: r0.append(r0[0])
                for i in range(0 if r0[0] == '' else int(r0[0]) - 1, pages_count if r0[1] == '' else int(r0[1])):
                    if i >= 0 and i < pages_count:
                        dupl_pagesB[i] = True
            return dupl_pagesB

        result = -1
        try:
            f1 = PdfEditorModel.objects.get(pk=form_id)
            existing_pdf = PdfReader(f1.file.path)
            pages_count = int(existing_pdf.numPages)
        except:
            result = 1
            return result, 'Undefined'
        new_pdf = PdfWriter()
        pages_to_duplicate = get_duplicate_pages_num(pages_count)
        copies = int(self.data.get('duplicate_copies', 0))
        duplicate_option = self.data.get('duplicate_option')
        from copy import copy
        if duplicate_option == PdfChooseModifyModel.PD_OPTION_01:
            for p in range(pages_count):
                for cp in range(1 + copies if pages_to_duplicate[p] else 1):
                    new_pdf.add_page(copy(existing_pdf.pages[p]))
        elif duplicate_option == PdfChooseModifyModel.PD_OPTION_02:
            #new_pdf.clone_document_from_reader(existing_pdf)
            for cp in range(1 + copies):
                for p in range(pages_count):
                    if cp == 0 or pages_to_duplicate[p]:
                        new_pdf.add_page(copy(existing_pdf.pages[p]))
        filename, dirname = get_filename(f1.file.path)
        newfile_fullpath = str(dirname)+"/"+filename+"-modify.pdf"
        with open(newfile_fullpath, "wb") as f:
            new_pdf.write(f)
        return result, newfile_fullpath
