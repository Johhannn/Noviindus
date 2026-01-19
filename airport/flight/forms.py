from django import forms
from .models import FlightNode, Route

class AddRouteNodeForm(forms.ModelForm):
    class Meta:
        model = FlightNode
        fields = ['route', 'parent', 'airport_code', 'node_type', 'duration']
        widgets = {
            'route': forms.Select(),
            'parent': forms.Select(),
            'airport_code': forms.TextInput(attrs={'placeholder': 'e.g., DEL'}),
            'node_type': forms.Select(),
            'duration': forms.NumberInput(attrs={'step': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = FlightNode.objects.all()
        self.fields['parent'].required = False


class CreateRouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name']

class NthSearchForm(forms.Form):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), required=True)
    start_node = forms.ModelChoiceField(queryset=FlightNode.objects.all(), required=False, label="Start Node (Default: Root)")
    n = forms.IntegerField(min_value=1, required=True, label="N (steps)")
    direction = forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right')], required=True)

class ShortestBetweenForm(forms.Form):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), required=False,
                                   help_text="(Optional) restrict search to a single route")
    airport_a = forms.CharField(max_length=10, label="Airport A")
    airport_b = forms.CharField(max_length=10, label="Airport B")
