from django import forms


class UploadFileForm(forms.Form):
    title = forms.Textarea()
    file = forms.FileField()
