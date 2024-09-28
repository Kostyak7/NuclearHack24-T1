from django.db import models


class FileForProccess(models.Model):
    file_path = "files"
    filename = models.TextField('Filename', unique=True)
    file_id = models.CharField("FileID", max_length=36, unique=True)
    is_ready = models.BooleanField("IsReady", default=False)
    lang = models.CharField("Language", max_length=3, default="RUS")
    upload_time = models.DateTimeField('Date-Time')

    def get_absolute_url(self):
        return f'{self.id}'
