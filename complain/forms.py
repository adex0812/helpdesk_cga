from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['username', 'user_id', 'description', 'complaint_type', 'file_path']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'user_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter user ID'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your complaint'}),
            'complaint_type': forms.Select(attrs={'class': 'form-control'}),
            'file_path': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UpdateStatusForm(forms.ModelForm):
    evidence = forms.FileField(required=False) #tambah sendiri 
    class Meta:
        model = Complaint
        fields = ['status', 'update_status_by', 'keterangan', 'evidence']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'update_status_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Updated by'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add notes'}),
        }