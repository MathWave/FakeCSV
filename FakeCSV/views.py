from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from FakeCSV.settings import DEFAULT_LOGIN_PAGE
from Main.models import DataSet


def enter(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/schemas')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
        return HttpResponseRedirect('/schemas')
    return render(request, 'enter.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(DEFAULT_LOGIN_PAGE)


def size(request):
    data = 'no data'
    with open('saved.json', 'r') as fs:
        data = fs.read()
    return HttpResponse(data)
