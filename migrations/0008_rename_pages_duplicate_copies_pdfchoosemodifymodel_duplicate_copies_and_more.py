# Generated by Django 4.0.6 on 2022-07-15 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PDF_editor', '0007_rename_pagesduplicatecopies_pdfchoosemodifymodel_pages_duplicate_copies_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdfchoosemodifymodel',
            old_name='pages_duplicate_copies',
            new_name='duplicate_copies',
        ),
        migrations.RenameField(
            model_name='pdfchoosemodifymodel',
            old_name='pages_duplicate_option',
            new_name='duplicate_option',
        ),
        migrations.AlterField(
            model_name='pdfeditormodel',
            name='file',
            field=models.FileField(default='Choose a file', upload_to='documents/'),
        ),
    ]