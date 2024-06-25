from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from rootapp.models import User, Project, ProjectMember, Task, Comment


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_again = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_passwords(self):
        pass1 = self.cleaned_data.get("password")
        pass2 = self.cleaned_data.get("password_again")
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords don't match!")
        return pass2

    def save(self, commit=True):
        """ Saves the provided password in hashed format. """

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_admin"]
    

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["username", "email", "password", "is_admin"]
    list_filter = ["is_admin"]
    search_fields = ["username", "email"]
    ordering = ["username"]
    filter_horizontal = []
    fieldsets = [
        ("Authentication", {"fields": ["username", "email", "password"]}),
        ("Personal Information", {"fields": ["first_name", "last_name", "date_joined"]}),
        ("Permission", {"fields": ["is_admin"]})
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["username", "email", "password", "password_again"]})
    ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register([Project, ProjectMember, Task, Comment])