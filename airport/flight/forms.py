from django import forms
from .models import AirportNode, Route

class AddRouteNodeForm(forms.ModelForm):
    class Meta:
        model = AirportNode
        fields = ['route', 'airport_code', 'position', 'duration']
        widgets = {
            'route': forms.Select(),
            'airport_code': forms.TextInput(attrs={'placeholder': 'e.g., DEL'}),
            'position': forms.NumberInput(),
            'duration': forms.NumberInput(attrs={'step': '0.1'}),
        }

class CreateRouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name']

class NthSearchForm(forms.Form):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), required=True)
    current_position = forms.IntegerField(min_value=1, required=True)
    n = forms.IntegerField(min_value=0, required=True, label="N (steps)")
    direction = forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right')], required=True)

class ShortestBetweenForm(forms.Form):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), required=False,
                                   help_text="(Optional) restrict search to a single route")
    airport_a = forms.CharField(max_length=10, label="Airport A")
    airport_b = forms.CharField(max_length=10, label="Airport B")
