from django import forms
from .models import Borrower
import re

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['ssn', 'bname', 'address', 'phone']
        widgets = {
            'bname': forms.TextInput(attrs={'style': 'width: 200px;'}),  # Adjust width here
        }
    def clean_ssn(self):
        ssn = self.cleaned_data['ssn']
        if not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
            raise forms.ValidationError("Invalid SSN format. Use XXX-XX-XXXX")
        if Borrower.objects.filter(ssn=ssn).exists():
            raise forms.ValidationError("Borrower with this SSN already exists.")
        return ssn