from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from blog.models import *
from blog.forms import *
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('core:index',))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def view_profile(request, pk):
	if request.method == 'POST' and request.user.is_authenticated:
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('profile_view', pk=request.user.pk)
	elif request.user.is_authenticated:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)

	profile = get_object_or_404(Profile, pk=pk)
	posts = Post.objects.filter(author=profile.user.pk)
	comments = Comment.objects.filter(author=profile.user.pk)
	if request.user.is_authenticated:
		return render(request, 'registration/profile_view.html', {
			'profile': profile,
			'comments': comments,
			'posts': posts,
			'user_form': user_form,
			'profile_form': profile_form
		})
	else:
		return render(request, 'registration/profile_view.html', {
			'profile': profile,
			'comments': comments,
			'posts': posts,
		})