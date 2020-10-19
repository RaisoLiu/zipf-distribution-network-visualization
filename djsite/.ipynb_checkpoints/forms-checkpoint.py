from django import forms
from .models import Data_in_str, Data_in_addr


class Addr_Form(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Data_in_addr
        fields = ('file', 'key',)

class Search_Form(forms.ModelForm):

    class Meta:
        model = Data_in_str
        fields = ('target_str',)