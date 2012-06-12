# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
import datetime



def api_call(request, database, collection, query):
    return HttpResponse("it's alive!")
    
    
