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
