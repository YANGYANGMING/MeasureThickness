from django import forms
from django.forms import fields, widgets

class ChangepwdForm(forms.Form):
    old_pwd = fields.CharField(label='旧密码', max_length=32, widget=widgets.PasswordInput(attrs={'class': 'layui-input'}))
    new_pwd = fields.CharField(label='新密码', max_length=32, widget=widgets.PasswordInput(attrs={'class': 'layui-input'}))
    new_pwd_confirm = fields.CharField(label='重复新密码', max_length=32, widget=widgets.PasswordInput(attrs={'class': 'layui-input'}))