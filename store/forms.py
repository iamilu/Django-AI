'''
write a Review Form using ReviewRating Model
'''
from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Review'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Rating'})
        }