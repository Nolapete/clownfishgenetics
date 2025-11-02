from django import forms
from .models import Variety, Parent, Cross


class VarietyForm(forms.ModelForm):
    class Meta:
        model = Variety
        fields = ['name', 'species', 'genotype_pattern']


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['variety']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Improve the display of the Variety dropdown
        self.fields['variety'].queryset = Variety.objects.order_by('species', 'name')


class CrossForm(forms.ModelForm):
    class Meta:
        model = Cross
        fields = ['parent1', 'parent2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Improve the display of the Parent dropdowns
        self.fields['parent1'].queryset = Parent.objects.select_related('variety').order_by('variety__species',
                                                                                            'variety__name')
        self.fields['parent2'].queryset = Parent.objects.select_related('variety').order_by('variety__species',
                                                                                            'variety__name')

