from django import forms
#from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import User
#User = get_user_model()

class UserCreationForm(UserCreationForm):
#    email = forms.EmailField(required=True)
#    username = forms.CharField(required=True, max_length=20)

    class Meta(UserCreationForm.Meta):
         model = User
         fields = UserCreationForm.Meta.fields + ('email',)

#    def save(self, commit=True):
#        user = super(UserCreateForm, self).save(commit=False)
#        user.email = self.cleaned_data["email"]
#        if commit:
#            user.save()
#        return user
