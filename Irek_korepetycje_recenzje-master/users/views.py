from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ReviewForm
from .models import Review
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



'''
def rating(request):
    user = Profile.objects.get(user_id=userID)
    reviewer = request.user

    if request.method == 'POST':
        form = ratingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.reviewer = reviewer
            rating.user = user
            rating.save()
            return()
    else:
        r_form = ratingForm()
    
    context = {
        'r_from': form,
    }
    
    return render(request, 'users/profile.html', context)
'''


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def submit_review(request, user_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review.objects.get(reviewer__id=request.user.id, user__id=user_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            '''messages.success(request, 'Dziękujemy! Twoja recenzja została zaktualizowana.')'''
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.content = form.cleaned_data['content']
                data.user_id = user_id
                data.reviewer_id = request.user.id
                data.save()
                '''messages.success(request, 'Dziękujemy! Twoja recenzja została zapisana.')'''
                return redirect(url)
