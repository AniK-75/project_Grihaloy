from django import forms
from .models import Property, PROPERTY_TYPE_CHOICES, PropertyEditRequest, PropertyDeleteRequest

BD_CITY_CHOICES = [
    ('Dhaka', 'Dhaka'),
    ('Chattogram', 'Chattogram'),
    ('Sylhet', 'Sylhet'),
    ('Khulna', 'Khulna'),
    ('Rajshahi', 'Rajshahi'),
    ('Barishal', 'Barishal'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
    ('Cumilla', 'Cumilla'),
    ('Gazipur', 'Gazipur'),
    ('Narayanganj', 'Narayanganj'),
    ("Cox's Bazar", "Cox's Bazar"),
]

class PropertyForm(forms.ModelForm):
    city = forms.ChoiceField(choices=BD_CITY_CHOICES)

    class Meta:
        model = Property
        fields = [
            'title', 'description',
            'address', 'area', 'city',
            'property_type', 'bedrooms', 'bathrooms', 'size_sqft',
            'price', 'is_price_fixed', 'is_active',
            'negotiable' # <-- FIX: Added 'negotiable'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        self.fields['bedrooms'].widget.attrs.update({'id': 'id_bedrooms', 'type': 'number', 'min': '0', 'step': '1'})
        self.fields['bathrooms'].widget.attrs.update({'id': 'id_bathrooms', 'type': 'number', 'min': '0', 'step': '1'})
        self.fields['size_sqft'].widget.attrs.update({'id': 'id_size_sqft', 'type': 'number', 'min': '0', 'step': '50'})
        self.fields['price'].widget.attrs.update({'id': 'id_price', 'type': 'number', 'min': '0', 'step': '500'})
        self.fields['description'].widget.attrs.update({'rows': 4})

class PropertySearchForm(forms.Form):
    q = forms.CharField(label='Keyword', required=False)
    area = forms.CharField(required=False)
    city = forms.ChoiceField(choices=[('', 'Any City')] + BD_CITY_CHOICES, required=False)
    property_type = forms.ChoiceField(choices=[('', 'Any')] + PROPERTY_TYPE_CHOICES, required=False)
    min_price = forms.IntegerField(required=False, min_value=0)
    max_price = forms.IntegerField(required=False, min_value=0)
    ordering = forms.ChoiceField(
        choices=[('-created_at', 'Latest'), ('price', 'Price: Low to High'), ('-price', 'Price: High to Low')],
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})
        self.fields['ordering'].widget.attrs.update({'class': 'form-select'})

    def clean(self):
        data = super().clean()
        min_p, max_p = data.get('min_price'), data.get('max_price')
        if min_p and max_p and min_p > max_p:
            self.add_error('max_price', 'Max price must be greater than or equal to min price.')
        return data

class EditRequestForm(forms.ModelForm):
    class Meta:
        model = PropertyEditRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Explain why you need to edit this listing...'}),
        }

class DeleteRequestForm(forms.ModelForm):
    class Meta:
        model = PropertyDeleteRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Why do you want to delete this listing?'}),
        }