# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import logout
from django.core.mail import send_mail
from django.core.mail.message import BadHeaderError
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt

from wasaboo.models import ContactForm

from django.template import loader


def wasaboo(request):
    return render(request, "index.html")

def logout_view(request):
    logout(request) 
    return HttpResponseRedirect('/login/')

@csrf_exempt
def about(request):
    return render(request, "about.html")

@csrf_exempt
def politics(request):
    return render(request, "politics.html")


@csrf_exempt
def contact(request):
	subject = request.POST.get('topic', '')
	name = request.POST.get('name', '')
	message = request.POST.get('message', '')
	from_email = request.POST.get('email', '')
	html_message = loader.render_to_string(
		'/opt/myenv/wasaboo/wasaboo/templates/contact_response.html',
		{
			'user_msg': message,
			'user_name': name,
			'user_email':  from_email,
		}
	)

        if subject and message and from_email:
                try:
                    send_mail(subject, html_message, from_email, ['contact@wasaboo.com'], fail_silently=True)

                except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                return HttpResponseRedirect('/contact/thankyou/')
        else:
            return render_to_response('contact.html', {'form': ContactForm()})
    
        return render_to_response('contact.html', {'form': ContactForm()},
            RequestContext(request))

def thankyou(request):
        return render_to_response('thankyou.html')
    



def error_404(request):
        data = {}
        return render(request,'error_404.html', data)

def error_500(request):
        data = {}
        return render(request,'error_500.html', data) 
		

@csrf_exempt
def sitemap(request):
    return render(request, "sitemap.html")