from django.core.validators import FileExtensionValidator
from django.db import models


class FileUpload(models.Model):
    arquivo = models.FileField(validators=[FileExtensionValidator(
                               ['arff'])])
    upload_at = models.DateTimeField(auto_now_add=True)
    classificador = models.CharField(max_length=10)
