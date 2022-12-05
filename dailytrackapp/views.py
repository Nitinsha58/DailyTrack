from django.shortcuts import render, redirect
from .models import DailyTrack
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from .forms import DailyTrackForm
from datetime import datetime, date

# Create your views here.

# Home page to show report of the month.

@login_required(login_url='login') #This decorator is used to check if user is logged in else redirect that user.
def index(request):
    Data = DailyTrack.objects.filter(user = request.user, added__month = datetime.now().month, added__year = datetime.now().year).order_by('-added') # fetching data from database to show all current month addred prices 

    
    form = DailyTrackForm() # Creating context of the form from forms.py file



    # creating data for charts.
    labels = []
    income_data = []
    expense_data = []

    for object in Data:
        labels.append(object.added.day)
        income_data.append(object.income)
        expense_data.append(object.expense)

    income_data = income_data[::-1]
    labels = labels[::-1]
    expense_data = expense_data[::-1]


    # This is for adding values that are added the same day and showing them in the charts as a day total.
    k = 0
    for j in range(len(labels)-1):
        if labels[k] == labels[k+1]:
            labels.pop(k + 1)
            income_data[k] += int(income_data[k + 1])
            income_data.pop(k + 1)

            expense_data[k] += int(expense_data[k + 1])
            expense_data.pop(k + 1)
        else:
            k += 1

    # Setting the max limit for the y axis of the graph.=====================
    if income_data or expense_data:
        if max(income_data)> max(expense_data):
            max_amount_limit = max(income_data) 
        else:
            max_amount_limit = max(expense_data)
    max_amount_limit = 200
    
    if request.method == 'POST':
        form = DailyTrackForm(request.POST)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = request.user
            form.save()
        return redirect('/')


    context = {'tracker':Data, 'form':form, 'labels':labels, 'Total_income':sum(income_data), 'Total_expense':sum(expense_data), 'income':income_data,'expense':expense_data ,'max_amount': max_amount_limit,  }
    return render(request, 'dailytrackapp/index.html', context)


@login_required(login_url='login') #This decorator is used to check if user is logged in else redirect that user.
def delete(request, pk):
    item = DailyTrack.objects.get(id = pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request, 'dailytrackapp/delete.html', context)



@login_required(login_url='login') #This decorator is used to check if user is logged in else redirect that user.
def edit(request, pk):
    item = DailyTrack.objects.get(id = pk)

    form = DailyTrackForm(instance= item)
    if request.method == 'POST':
        form = DailyTrackForm(request.POST, instance = item)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = request.user
            form.save()
        return redirect('/')

    context = {'form': form, 'item': item}
    return render(request, 'dailytrackapp/edit.html', context)


@login_required(login_url='login') #This decorator is used to check if user is logged in else redirect that user.
def search(request):
    d = date.today()
    search_date = str(datetime.now().year)+ "-" + f"{d.month:02d}"
    print(search_date)
    if request.method == "POST":
        month_year = request.POST['month_year']
        if not month_year:
            return redirect('/search/')

        year, month = month_year.split('-')
        filtered_amounts = DailyTrack.objects.filter(user = request.user, added__month = month, added__year = year ).order_by('-added')


        labels = []
        income_data = []
        expense_data = []

        for object in filtered_amounts:
            labels.append(object.added.day)
            income_data.append(object.income)
            expense_data.append(object.expense)
        labels = labels[::-1]
        income_data = income_data[::-1]
        expense_data = expense_data[::-1]


        # This is for adding values that are added the same day and showing them in the charts as a day total.
        k = 0
        for _ in range(len(labels)-1):
            if labels[k] == labels[k+1]:
                labels.pop(k + 1)
                income_data[k] += int(income_data[k + 1])
                income_data.pop(k + 1)

                expense_data[k] += int(expense_data[k + 1])
                expense_data.pop(k + 1)
            else:
                k += 1

        # Setting the max limit for the y axis of the graph.=====================
        max_amount_object = DailyTrack.objects.filter(user = request.user)
        max_amount_list = []
        if income_data or expense_data:
            max_amount_limit = max(max(income_data), max(expense_data))
        else: 
            max_amount_limit = 200

        context = {'results': filtered_amounts, 'Total_income':sum(income_data), 'Total_expense':sum(expense_data), 'labels':labels, 'data':income_data, 'expense':expense_data,'date':search_date, 'max_amount':max_amount_limit}

        return render(request, 'dailytrackapp/search.html', context)
    return render(request, 'dailytrackapp/search.html', {'date':search_date})


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'User or Password is incorrect.')
            return redirect('login')
    return render(request, 'dailytrackapp/login.html')


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save() 
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was create for {user}')
            return redirect('login') 
        else:
            messages.error(request, 'In valid creadentials.')
            return redirect('register')
    context = {'form': form}
    return render(request, 'dailytrackapp/register.html', context)


def view_data(request, pk):
    Data = DailyTrack.objects.get(pk = pk) # fetching data from database to show the selected data
    print(Data)

    context = {'data':Data,}
    return render(request, 'dailytrackapp/view_data.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
