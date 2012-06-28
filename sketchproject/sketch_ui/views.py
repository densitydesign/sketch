# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader

def index(request):
    c = RequestContext(request)
    return render_to_response("sketch_ui/index.html", {}, context_instance = c)
    
    
