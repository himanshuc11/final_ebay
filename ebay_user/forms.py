from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class register_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Create a login Form
class login_form(AuthenticationForm):
    class Meta:
        model = User