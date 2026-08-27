from django.shortcuts import render, redirect
from calory_counter_app.models import *
from calory_counter_app.forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Sum


def register_view(request):

    form_data = userForm()

    if request.method == 'POST':

        form_data = userForm(request.POST)

        if form_data.is_valid():

            form_data.save()
            return redirect('login_view')

    context = {
        'form_data' : form_data
    }

    return render(request, 'register.html', context)


def login_view(request):

    form_data = AuthenticationForm()

    if request.method == 'POST':

        form_data = AuthenticationForm(request, data = request.POST)

        if form_data.is_valid():

            user = form_data.get_user()
            login(request, user)
            return redirect('dashboard')

    context = {
        'form_data' : form_data
    }

    return render(request, 'login.html', context)


@login_required
def logout_view(request):

    logout(request)

    return redirect('login_view')


@login_required
def dashboard(request):

    today_consumed_data = consumedColorieModel.objects.filter(
        consumed_by=request.user,
        created_at = date.today()
    )

    total_consumed_calories = today_consumed_data.aggregate(total=Sum('calorie'))

    try:
        calorie_required = profileModel.objects.get(user=request.user).bmr
    except profileModel.DoesNotExist:
        return redirect('profile_update')

    sum_calory = round(float(total_consumed_calories['total'] or 0.00), 2)

    if sum_calory < calorie_required:
        suggestion = 'You consumed less calorie today, eat more!'
    else:
        suggestion = 'You consumed more calorie today, eat less!'

    context = {
        'calorie_required' : calorie_required,
        'total_consumed_calories' : sum_calory,
        'today_consumed_data' : today_consumed_data,
        'less_more' : round(calorie_required - sum_calory, 2),
        'suggestion' : suggestion,
    }

    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):

    try:
        user_data = profileModel.objects.get(user=request.user)
    except:
        user_data = profileModel.objects.create(user=request.user)

    context = {
        'user_data' : user_data,
    }

    return render(request, 'profile_view.html', context)

@login_required
def profile_update(request):

    try:
        user_data = profileModel.objects.get(user=request.user)
    except:
        user_data = profileModel.objects.create(user=request.user)

    form_data = profileUpdateForm(instance=user_data)

    if request.method == 'POST':
        form_data_partial = profileUpdateForm(request.POST, instance=user_data)
        if form_data_partial.is_valid():
            form_data = form_data_partial.save(commit=False)
            age = int(form_data.age)
            height = float(form_data.height)
            weight = float(form_data.weight)
            if form_data.gender == 'Male':
                form_data.bmr = round(66.47 + (13.75*weight) + (5.003*height) - (6.755*age), 2)
            elif form_data.gender == 'Female':
                form_data.bmr = round(655.1 + (9.563*weight) + (1.85*height) - (4.676*age), 2)
            else:
                form_data.bmr = 0
            form_data.save()
            return redirect('profile_view')

    context = {
        'form_data' : form_data,
    }

    return render(request, 'profile_update.html', context)


@login_required
def calorie_list(request):

    data = consumedColorieModel.objects.filter(consumed_by=request.user)

    context = {
        'data' : data,
    }

    return render(request, 'calorie_list.html', context)

@login_required
def add_consumed_calorie(request):

    form_data = calorieConsumedForm()

    if request.method == 'POST':
        form_data = calorieConsumedForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()
            return redirect('calorie_list')

    context = {
        'form_data' : form_data,
    }

    return render(request, 'add_consumed_calorie.html', context)


@login_required
def edit_consumed_calorie(request, c_id):

    data = consumedColorieModel.objects.get(id=c_id)

    form_data = calorieConsumedForm(instance=data)

    if request.method == 'POST':
        form_data = calorieConsumedForm(request.POST, instance=data)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()
            return redirect('calorie_list')

    context = {
        'form_data' : form_data,
    }

    return render(request, 'edit_consumed_calorie.html', context)

@login_required
def delete_consumed_calorie(request, c_id):

    consumedColorieModel.objects.get(id=c_id).delete()
    return redirect('calorie_list')