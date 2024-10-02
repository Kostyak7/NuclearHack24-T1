import os
from celery import shared_task
from .models import FileForProccess
from algorithms.text_analysis import toc_process_pdf_file


@shared_task
def process_form_data_async(data_id):
    try:
        form_data = FileForProccess.objects.get(id=data_id)
        
        filepath = os.path.join(os.getcwd(), FileForProccess.file_path + '/' + form_data.filename)
        hints = {}
        if form_data.has_toc_hint is not None:
            if form_data.has_toc_hint and form_data.toc_end_hint >= form_data.toc_start_hint > 0:
                hints = {
                    'has_toc': True,
                    'toc_range': [form_data.toc_start_hint, form_data.toc_end_hint] 
                }
            else:
                hints = {
                    'has_toc': False,
                    'toc_range': [None] * 2
                }
        
        toc_process_pdf_file(filepath, lang=form_data.lang.lower(), hints=hints)

        print("HOORAY!")
        form_data.is_ready = True
        form_data.save()
    except FileForProccess.DoesNotExist:
        pass
    except:
        pass