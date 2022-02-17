from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('UserProfile')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('Login')
    else:
        return render(request, 'Accounts/Login.html')


def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out!')
        return redirect('RISDB')


def Register(request):
    if request.method == 'POST':
        # Get Form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # check if password match
        if password == password2:
            # Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That Username is taken')
                return redirect('Register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That Email is Registered')
                    return redirect('Register')
                else:
                    # Adding User to DB
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    # Login After Register
                    # auth.login(request, user)

                    # Redirect To Login Page After Register
                    user.save()
                    messages.success(request, 'You are now logged in!')
                    return redirect('Login')
        else:
            messages.error(request, 'Passwords Do Not Match.')
            return redirect('Register')
    else:
        return render(request, 'Accounts/Register.html')


def UserProfile(request):
    # Get the user submitted dashboards only
    Users_Dashboards = Dashboard.objects.order_by('-Submission_Date').filter(user_id=request.user.id)
    Users_Dashboards_count = len(Users_Dashboards)
    context = {
        'Category_Choices': Category_Choices,
        'Users_Dashboards': Users_Dashboards,
        'Users_Dashboards_count': Users_Dashboards_count
    }
    return render(request, r'Accounts/UserProfile.html', context)

# def DashboardSubmission(request):
#     if request.method == 'POST':
#         dashboard_submission = Dashboard()
#         dashboard_submission.Title = request.POST['Title']
#         dashboard_submission.Author = request.POST['Author']
#         dashboard_submission.Thumbnail = request.FILES['Thumbnail']
#         dashboard_submission.Dashboard_URL_Link = request.POST['Dashboard_URL_Link']
#         dashboard_submission.Short_Description = request.POST['Short_Description']
#         dashboard_submission.Category = request.POST['Category']
#         dashboard_submission.user_id = request.POST['user_id']
#         # Check if User has submitted this dashboard
#         # To be implemented
#
#         dashboard_submission.save()
#         messages.success(request, 'Your Dashboard has been posted, thank you!')
#         return redirect('UserProfile')
#     else:
#         messages.error(request, 'Problem in submission. Please Try Again!')
#         return render(request, r'Accounts\UserProfile.html')