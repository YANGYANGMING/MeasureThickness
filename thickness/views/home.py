from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views import View
from utils.myforms import ChangepwdForm


class IndexView(View):
    """首页"""
    def get(self, request, *args, **kwargs):

        return render(request, "index.html")

class ChangepwdView(View):
    """修改密码"""
    def get(self, request, *args, **kwargs):
        """修改密码"""
        result = {'message': ''}
        form = ChangepwdForm()
        if not request.user.is_authenticated:
            result['message'] = '未登录'
            print('未登录')
        return render(request, "thickness/change_pwd.html", locals())

    def post(self, request, *args, **kwargs):
        result = {'message': ''}
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            old_pwd = form.cleaned_data['old_pwd']
            new_pwd = form.cleaned_data['new_pwd']
            new_pwd_confirm = form.cleaned_data['new_pwd_confirm']
            user = authenticate(username=request.user, password=old_pwd)
            if user:  # 旧密码正确
                if new_pwd == new_pwd_confirm:  # 两次新密码一致
                    user.set_password(new_pwd)
                    user.save()
                    print('更改成功')
                    return redirect('/login/')
                else:  # 两次新密码不一致
                    result['message'] = '两次密码不一致'
                    return render(request, 'thickness/change_pwd.html', locals())
            else:
                result['message'] = '旧密码错误'
                return render(request, 'thickness/change_pwd.html', locals())



