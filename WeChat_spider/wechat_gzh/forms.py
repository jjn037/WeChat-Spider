from django import forms
from wechat_gzh.models import GZH


class GZHForm(forms.Form):
    # name = forms.CharField(max_length=50)
    weixin_id = forms.CharField(max_length=50, label='微信号')

    class Meta:

        fields = ('weixin_id',)