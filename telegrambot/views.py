from django.shortcuts import render
from .models import TelegramUser


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        data_of_users = TelegramUser.objects.all()
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        url_user_tg_account = f"https://t.me/{username}"

        if username in data_of_users.get(username=username).username:
            data_of_user = data_of_users.get(username=username)
            print(data_of_user)
            if data_of_user.password == password:
                context = {
                    "password": password,
                    "username": username,
                    "full_name": f"{data_of_user.first_name} {data_of_user.last_name}",
                    "id": f"{data_of_user.id}",
                    "url_user_tg_account": url_user_tg_account,
                }

                return render(request, "index.html", context=context)
        else:
            error_contex = {
                "errors": "Invalid credentials"
            }

            return render(request, "login.html", context=error_contex)

def base_view(request):
    return render(request, 'base.html')
