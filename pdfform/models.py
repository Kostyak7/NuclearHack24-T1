from django.db import models


class FileForPrint(models.Model):
    file_path = "files"
    filename = models.TextField('Filename', unique=True)
    upload_time = models.DateTimeField('Date-Time')
    case_type = models.CharField("Format", max_length=8, default="STANDART")

    def get_absolute_url(self):
        return f'{self.id}'
