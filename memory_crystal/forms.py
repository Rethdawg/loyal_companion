from django import forms
from .models import Memo, Category
from tinymce.widgets import TinyMCE


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ('title', 'category', 'content')
        widgets = {
            'content': TinyMCE(),
            'pub_date': forms.HiddenInput,
            'last_modified': forms.HiddenInput
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
