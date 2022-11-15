from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignInForm


def index(request):
    # import pdb; pdb.set_trace()
    return render(request, 'home/home.html')


# def login(request):
#     # import pdb; pdb.set_trace()
#     return render(request, 'login.html')


def login_membro(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)

        if form.is_valid():
            print(request)
            username = request.POST['username']
            password = request.POST['password']
            membro = authenticate(request, username=username, password=password)
            print(membro)
            if membro is not None:

                login(request, membro)
                return redirect('contratos_list')
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form})


def sair(request):
    print(request)
    logout(request)
    return redirect('index')
