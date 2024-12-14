from django import forms
from finance_site.models import Finance_site, Category


class AddOperationForm(forms.ModelForm):
    cat1 = forms.ModelChoiceField(queryset=Category.objects.filter(type=0), label='Категории', required=False)
    cat2 = forms.ModelChoiceField(queryset=Category.objects.filter(type=1), label='Категории', required=False)

    class Meta:
        model = Finance_site
        fields = ['operation_type', 'operation_name', 'amount', 'notes']
        widgets = {
            'operation_name': forms.TextInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

    def clean_cat_id(self):
        cleaned_data = super().clean()
        field1_value = cleaned_data.get('cat1')
        field2_value = cleaned_data.get('cat2')

        if field1_value:
            cleaned_data['cat'] = field1_value
        else:
            cleaned_data['cat'] = field2_value
        return cleaned_data

