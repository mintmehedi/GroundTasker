from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_type', 'due_date', 'location', 'description', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Clean my kitchen'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Wollongong NSW, 2500'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write more details about the task…', 'rows': 4}),
            'budget': forms.NumberInput(attrs={'placeholder': '$100'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
