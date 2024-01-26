from django import forms
from .models import Memo, Category, Birthday, BirthdayNote
from tinymce.widgets import TinyMCE


# class BaseMemoFormset(forms.BaseFormSet):
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#         form.fields['new category'] = forms.CharField(max_length=200, required=False)


class MemoForm(forms.ModelForm):
    """
    Form class for the Memo model.
    """
    class Meta:
        model = Memo
        fields = ('title', 'category', 'content')
        widgets = {
            'content': TinyMCE(),
            'pub_date': forms.HiddenInput,
            'last_modified': forms.HiddenInput
        }


# MemoFormSet = forms.formset_factory(MemoForm,  formset=BaseMemoFormset)


class CategoryForm(forms.ModelForm):
    """
    Form class for the Category model.
    """
    class Meta:
        model = Category
        fields = ('name',)


class BirthdayForm(forms.ModelForm):
    """
    Form class for the birthday model.
    """
    class Meta:
        model = Birthday
        fields = ('person', 'bdate')


class BirthdayNoteForm(forms.ModelForm):
    """
    Form class for the BirthdayNote model.
    """
    class Meta:
        model = BirthdayNote
        fields = ('title', 'content')
        widgets = {
            'content': TinyMCE(),
            'pub_date': forms.HiddenInput,
            'birthday': forms.HiddenInput
        }
