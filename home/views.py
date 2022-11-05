from django.shortcuts import render


def index(request):
    # import pdb; pdb.set_trace()
    return render(request, 'home/home.html')


def login(request):
    # import pdb; pdb.set_trace()
    return render(request, 'login.html')
