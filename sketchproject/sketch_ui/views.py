# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def index(request):
    c = RequestContext(request)
    return render_to_response("sketch_ui/index.html", {}, context_instance = c)
    
    

@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
    # Redirect to a success page.