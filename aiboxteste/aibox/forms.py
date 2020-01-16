from django import forms

from aibox.models import FileUpload


class FileUploadForm(forms.ModelForm):
    CHOICES = (
        (1, 'SVM'),
        (2, 'KNN'),
        (3, 'Random Florest'),
    )

    classificador = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = FileUpload
        fields = ('arquivo', 'classificador', )
