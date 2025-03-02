from django import forms
from .models import CustomUser  # Import the custom user model

class CustomUserCreationForm(forms.ModelForm):
    # Add a confirmation field for password to check if passwords match
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        help_text="Enter the same password again for verification."
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name']  # Only these fields are included in the form

    def clean_password2(self):
        # Check if password1 and password2 are the same
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return password2

    def save(self, commit=True):
        # Save the user instance with hashed password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        
        return user
