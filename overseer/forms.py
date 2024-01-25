from django import forms
from .models import Task, SubTask
from tinymce.widgets import TinyMCE


class TaskForm(forms.ModelForm):
    """
    Class describing the form used for Task instances.
    """
    class Meta:
        model = Task
        fields = ('title', 'due_date')
        widgets = {
            'pub_date': forms.HiddenInput
        }


TaskFormSet = forms.inlineformset_factory(Task, SubTask,
                                          fields=('title', 'due_date', 'content', 'status'))


class SubtaskForm(forms.ModelForm):
    """
    Class describing the form used for Subtask instances.
    """
    class Meta:
        model = SubTask
        fields = ('title', 'due_date', 'status', 'content',)
        widgets = {
            'pub_date': forms.HiddenInput,
            'content': TinyMCE(),
            'main_task': forms.HiddenInput
        }
