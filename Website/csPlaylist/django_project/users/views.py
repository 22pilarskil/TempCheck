from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import pymongo


def customSave(phone1, phone2, email1, email2, username):
    connectionURL = f"mongodb+srv://Zayn-Rekhi:assimo11!@tempcheck.cfwko.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connectionURL)
    mydb=client["LeptonData"]
    mainCollection=mydb["Profile"]

    data = {"phone1":phone1,"phone2":phone2,"email1":email1,"email2":email2,"username":username}
    find = mainCollection.find_one({"username":username})
    
    if not find:
        mainCollection.insert_one(data)
    elif find["phone1"] and find["phone2"] and find["email1"] and find["email2"] and find["username"]:
        query = {"username":username}
        mainCollection.replace_one(query, data)

def getInfo(user):
    connectionURL = f"mongodb+srv://Zayn-Rekhi:assimo11!@tempcheck.cfwko.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connectionURL)
    mydb=client["LeptonData"]
    mainCollection=mydb["Profile"]

    find = mainCollection.find_one({"username":user})
    if not find:
        return "", "", "", ""
    else:
        return find["email1"], find["email2"], find["phone1"], find["phone2"]

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
    username = request.user.username
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        phone1 = request.POST.get("phone1")
        phone2 = request.POST.get("phone2")

        email1  = request.POST.get("email1")
        email2  = request.POST.get("email2")

        
        if u_form.is_valid() and p_form.is_valid():
            customSave(phone1, phone2, email1, email2, username)
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)



    email1, email2, phone1, phone2 = getInfo(username)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'email1':email1,
        'email2':email2,
        'phone1':phone1,
        'phone2':phone2,
    }

    return render(request, 'users/profile.html', context)
