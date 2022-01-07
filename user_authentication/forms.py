from django import forms
from .models import User


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')



