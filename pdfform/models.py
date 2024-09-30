from django.db import models


class FileForProccess(models.Model):
    file_path = "files"
    filename = models.TextField('Filename', unique=True)
    file_id = models.CharField("FileID", max_length=36, unique=True)
    is_ready = models.BooleanField("IsReady", default=False)
    lang = models.CharField("Language", max_length=3, default="RUS")
    upload_time = models.DateTimeField('Date-Time')
    
    has_toc_hint = models.BooleanField("HasTOC", null=True, blank=True)
    toc_start_hint = models.IntegerField("StartTOC", default=-1)
    toc_end_hint = models.IntegerField("EndTOC", default=-1)

    def get_absolute_url(self):
        return f'{self.id}'
