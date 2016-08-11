from django import forms
from wechat_gzh.models import GZH


class GZHForm(forms.Form):
    weixin_id = forms.CharField(max_length=50, label='微信号')

    class Meta:
        fields = ('weixin_id',)


class Fuzzy_search(forms.Form):
    key = forms.CharField(max_length=50, label='关键字', required=False)

    class Meta:
        fields = ('key',)
