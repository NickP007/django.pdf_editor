from django.db import models


# Create your models here.
class PdfEditorModel(models.Model):
    # fields of the model
    author = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='documents/', default='Choose a file')

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.title


class PdfChooseModifyModel(models.Model):
    # id = models.AutoField()
    PD_OPTION_01 = 'CP'
    PD_OPTION_02 = 'JE'
    PAGE_DUPLICATE_OPTION_CHOISES = [
        (PD_OPTION_01, 'Collate Pages'),
        (PD_OPTION_02, 'Join to End'),
    ]
    pages_to_duplicate = models.CharField(max_length=100)
    pages_duplicate_copies = models.IntegerField(default=1)
    pages_duplicate_option = models.CharField(max_length=2, choices=PAGE_DUPLICATE_OPTION_CHOISES, default=PD_OPTION_01)

    def __str__(self):
        return str(self.PagesDuplicateOption)