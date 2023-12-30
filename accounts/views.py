from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.

def register_view(request):
    form =UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        print(user)
        return redirect('/login')
    print(form.is_valid())
    return render(request, "accounts/register.html", context={"form": form})

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
    else:
        form = AuthenticationForm(request)
    
    context['form'] = form
    return render(request, "accounts/login.html", context=context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')
    return render(request, "accounts/logout.html", context={})