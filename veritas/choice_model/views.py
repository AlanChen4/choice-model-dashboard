from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import ModifiedSitesBundle, Site, ModifiedSite
from .utils import ChoiceModel

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .dashapps import site_choice_prob


class BundleList(LoginRequiredMixin, ListView):
    model = ModifiedSitesBundle
    context_object_name = 'bundles'
    template_name = 'bundles.html'

    def get_queryset(self):
        return super().get_queryset().filter(history_id=self.request.user)


class BundleDetail(LoginRequiredMixin, DetailView):
    model = ModifiedSitesBundle
    context_object_name = 'bundle'
    template_name = 'bundle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get list of modified sites from bundle_id
        bundle_id = context['bundle'].bundle_id
        modified_sites = list(ModifiedSite.objects.all().filter(bundle_id=bundle_id))

        choice_model = ChoiceModel()
        site_choice_probs = choice_model.get_site_choice_visit_prob(modified_sites)
        visitation_probability = choice_model.get_visitation_probability(modified_sites)

        baseline_equity_evaluation  = choice_model.get_equity_evaluation([])
        equity_evaluation = choice_model.get_equity_evaluation(modified_sites)

        # for bubble plot
        site_choice_prob_labels = list(site_choice_probs.keys())
        site_choice_prob_values = list(site_choice_probs.values())
        site_choice_prob_sizes = [min(site * 1000, 500) for site in site_choice_prob_values]
        bubble_fig = go.Figure(data=[go.Scatter(
            x=site_choice_prob_labels,
            y=site_choice_prob_values,
            marker_size=site_choice_prob_sizes,
            mode='markers',
        )])
        bubble_fig.update_layout(
            margin=dict(l=20, r=20, b=5, t=5),
        )

        # for scatter map
        site_location_and_prob = pd.merge(
            visitation_probability.mean(axis=1).to_frame(),
            choice_model.site_and_location,
            left_index=True, right_index=True
        )
        site_location_and_prob = site_location_and_prob.rename(columns={0: 'Visitation Probability'})
        site_location_and_prob = site_location_and_prob.reset_index()
        map_scatter_fig = px.scatter_mapbox(
            site_location_and_prob,
            lat='latitude', 
            lon='longitude', 
            color='Visitation Probability', 
            size='Visitation Probability', 
            hover_name='name')
        map_scatter_fig.update_layout(mapbox_style='open-street-map')

        context['dash_context'] = {
            'bubble-plot': {'figure': bubble_fig},
            'map-scatter-plot': {'figure': map_scatter_fig}
        }

        context['baseline_equity_black'] = round(baseline_equity_evaluation['average_utility_black'], 3)
        context['baseline_equity_other'] = round(baseline_equity_evaluation['average_utility_other'], 3)
        context['counterfactual_equity_black'] = round(equity_evaluation['average_utility_black'], 3)
        context['counterfactual_equity_other'] = round(equity_evaluation['average_utility_other'], 3)

        return context

    def get_queryset(self):
        return super().get_queryset().filter(history_id=self.request.user)


class BundleCreate(LoginRequiredMixin, CreateView):
    model = ModifiedSitesBundle
    fields = ['nickname']
    success_url = reverse_lazy('bundles')
    template_name = 'bundle_create.html'

    def form_valid(self, form):
        form.instance.history_id = self.request.user
        return super().form_valid(form)


class BundleUpdate(LoginRequiredMixin, UpdateView):
    model = ModifiedSitesBundle
    fields = ['nickname']
    success_url = reverse_lazy('bundles')
    context_object_name = 'bundle'
    template_name = 'bundle_modify.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bundle_id = context['bundle'].bundle_id
        context['bundle_id'] = bundle_id
        if self.request.GET.get('modified-only') == 'on':
            context['modified'] = True
            context['sites'] = ModifiedSite.objects.all().filter(bundle_id=bundle_id).order_by('name')
        else:
            context['modified'] = False
            context['sites'] = Site.objects.all().order_by('name')
        return context

    def get_queryset(self):
        return super().get_queryset().filter(history_id=self.request.user)


class BundleDelete(LoginRequiredMixin, DeleteView):
    model = ModifiedSitesBundle
    context_object_name = 'bundle'
    success_url = reverse_lazy('bundles')
    template_name = 'bundle_confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(history_id=self.request.user)


class ModifiedSiteCreate(LoginRequiredMixin, CreateView):
    model = ModifiedSite
    fields = ['name', 'acres', 'trails', 'trail_miles', 'picnic_area', 'sports_facilities', 
              'swimming_facilities', 'boat_launch', 'waterbody', 'bathrooms', 'playgrounds']
    template_name = 'modified_site_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # calculate bundle_id from url and add to context
        bundle_id = self.request.path.split('/')[2]
        context['bundle_id'] = bundle_id

        return context

    def get_initial(self):
        initial =  super().get_initial()

        # check if there is existing modified site
        bundle_id = self.request.path.split('/')[2]
        site_name = self.request.path.split('/')[3]
        if ModifiedSite.objects.all().filter(bundle_id=bundle_id).filter(name=site_name).exists():
            site = ModifiedSite.objects.all().filter(bundle_id=bundle_id).get(name=site_name)
        else:
            # get original data belonging to site
            site = Site.objects.get(name=site_name)

        initial = {
            'name': site.name,
            'acres': site.acres,
            'trails': site.trails,
            'trail_miles': site.trail_miles,
            'picnic_area': site.picnic_area,
            'playgrounds': site.playgrounds,
            'sports_facilities': site.sports_facilities,
            'swimming_facilities': site.swimming_facilities,
            'boat_launch': site.boat_launch,
            'waterbody': site.waterbody,
            'bathrooms': site.bathrooms
        }

        return initial

    def get_success_url(self):
        bundle_id = self.request.path.split('/')[2]
        return reverse_lazy('bundle-update', kwargs={'pk': bundle_id})

    def form_valid(self, form):
        bundle_id = self.request.path.split('/')[2]

        form.instance.history_id = self.request.user
        form.instance.bundle_id = ModifiedSitesBundle.objects.get(bundle_id=bundle_id)

        if ModifiedSite.objects.filter(bundle_id=bundle_id).filter(name=form.instance.name).exists():
            ModifiedSite.objects.filter(bundle_id=bundle_id).filter(name=form.instance.name).delete()

        return super().form_valid(form)
