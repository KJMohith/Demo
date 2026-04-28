from django import forms

from .models import Event, Participant
from .validators import validate_photo, validate_receipt


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('name', 'email', 'transaction_id', 'receipt', 'photo')

    def clean_transaction_id(self):
        transaction_id = self.cleaned_data['transaction_id']
        if Participant.objects.filter(transaction_id=transaction_id).exists():
            raise forms.ValidationError('This transaction ID is already registered.')
        return transaction_id

    def clean_receipt(self):
        receipt = self.cleaned_data['receipt']
        validate_receipt(receipt)
        return receipt

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        validate_photo(photo)
        return photo


class FeedbackForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='Comment')

    class Meta:
        model = Participant
        fields = ('rating',)
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'event_date', 'description')
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
