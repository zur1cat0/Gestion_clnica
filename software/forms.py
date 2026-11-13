from django import forms

from .models import IntervencionSoftware


class IntervencionSoftwareForm(forms.ModelForm):
    class Meta:
        model = IntervencionSoftware
        fields = ["tecnico", "diagnostico", "solucion", "siguiente_paso"]
        widgets = {
            "tecnico": forms.TextInput(attrs={"class": "form-control"}),
            "diagnostico": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "solucion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "siguiente_paso": forms.Select(attrs={"class": "form-select"}),
        }
