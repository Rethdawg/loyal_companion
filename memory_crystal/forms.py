from django import forms
from .models import Memo, Category, Birthday, BirthdayNote
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


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = ('person', 'bdate')


class BirthdayNoteForm(forms.ModelForm):
    class Meta:
        model = BirthdayNote
        fields = ('title', 'content')
        widgets = {
            'content': TinyMCE(),
            'pub_date': forms.HiddenInput,
            'birthday': forms.HiddenInput
        }
