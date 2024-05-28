from django.shortcuts import render
import Django.UniMatch.ai_logic.data_extraction.data_scarp_pdf as dsp

# Create your views here.

def index(request):
    program_list = dsp.fetch_page_content('cbu.ac.zm')
    return render(request=request,template_name="index.html")