from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        error_msg = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        rmb = request.POST.get('rmb')

        user = authenticate(username=username, password=password)
        if user:
            print("passed authentication")
            login(request, user)  # 把user封装到request.session中
            if rmb:
                request.session.set_expiry(60 * 60 * 24 * 30)
                print('rmb')
            return redirect(request.GET.get('next', '/thickness/index'))  # 登录后跳转至next指定的页面，否则到首页
        else:
            error_msg = "用户名或密码错误!"

        return render(request, 'login.html', locals())


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login/')


