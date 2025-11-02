from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Variety, Parent, Cross, Progeny
from .forms import VarietyForm, ParentForm, CrossForm
# from .services import perform_cross_calculation # Assuming a service function exists

# --- Variety Views ---

class VarietyListView(ListView):
    model = Variety
    template_name = 'calcRefactor/variety_list.html'
    context_object_name = 'varieties'

class VarietyDetailView(DetailView):
    model = Variety
    template_name = 'calcRefactor/variety_detail.html'
    context_object_name = 'variety'

class VarietyCreateView(CreateView):
    model = Variety
    form_class = VarietyForm
    template_name = 'calcRefactor/variety_form.html'
    success_url = reverse_lazy('variety-list')

# --- Parent Views ---

class ParentListView(ListView):
    model = Parent
    template_name = 'calcRefactor/parent_list.html'
    context_object_name = 'parents'

class ParentCreateView(CreateView):
    model = Parent
    form_class = ParentForm
    template_name = 'calcRefactor/parent_form.html'
    success_url = reverse_lazy('parent-list')

# --- Cross Views ---

class CrossListView(ListView):
    model = Cross
    template_name = 'calcRefactor/cross_list.html'
    context_object_name = 'crosses'

class CrossDetailView(DetailView):
    model = Cross
    template_name = 'calcRefactor/cross_detail.html'
    context_object_name = 'cross'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progeny'] = self.object.progeny_set.all()
        return context

class CrossCreateView(CreateView):
    model = Cross
    form_class = CrossForm
    template_name = 'calcRefactor/cross_form.html'
    success_url = reverse_lazy('cross-list')

# --- Calculation View (Function-Based) ---
def calculate_cross_results(request, cross_id):
    cross = get_object_or_404(Cross, pk=cross_id)
    # This view would typically call a service function to get results
    # results = perform_cross_calculation(cross)
    results = [ # Placeholder results
        {'phenotype': 'Picasso', 'genotype': 'AB', 'ratio': '50%'},
        {'phenotype': 'Snowflake', 'genotype': 'AA', 'ratio': '50%'},
    ]

    context = {
        'cross': cross,
        'results': results,
    }
    return render(request, 'calcRefactor/cross_results.html', context)
