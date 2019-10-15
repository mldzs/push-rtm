import json
import operator
from functools import reduce

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.contrib import messages

from smartmin.views import SmartCreateView, SmartListView, SmartTemplateView

from .models import Flow
from .forms import FlowForm

class RTMBaseListView(SmartListView):
    search_query_name = 'search'

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        return self.search(queryset)

    """
    def filter(self, queryset):
        sort_field = self.request.GET.get('sort')
        sort_direction = self.request.GET.get('dir')
        page = self.request.GET.get('page')
        #language = self.request.GET.get('lang', '')
        #sdg = self.request.GET.get('sdg', 0)

        filters = {}
        sortered = "pk"

        #if language: filters['languages__contains'] = list(language)
        #if sdg: filters['sdgs__contains'] = list(sdg)
       if 
    
    
        
        
        
        if sort_field:
            sortered = "{}{}".format("-" if sort_direction == "desc" else "", sort_field)
        
        queryset.filter
    """


    def search(self, queryset):
        '''
        It receives the queryset parameters, applies the filter and returns the queryset.
        This method requires the class to have the 'search_fields' and 'search_query_name' atrributes.
        eg:
        search_fields = ['title__icontains', 'description__icontains']
        search_query_name = 'search' # in template, this attribute is an input name by search field
        '''
        search_query = self.request.GET.get(self.search_query_name)
        search_fields = self.derive_search_fields()

        if search_fields and search_query:
            term_queries = []
            for term in search_query.split(' '):
                field_queries = []
                for field in search_fields:
                    field_queries.append(Q(**{field: term}))
                term_queries.append(reduce(operator.or_, field_queries))

            queryset = queryset.filter(reduce(operator.and_, term_queries))
        
        # add any select related
        related = self.derive_select_related()
        if related:
            queryset = queryset.select_related(*related)
        
        return queryset


class ListView(RTMBaseListView):
    template_name = 'flowhub/index.html'
    #permission = 'flowhub.flow_list'
    model = Flow
    context_object_name = 'flows'
    search_fields = ['name__icontains','description__icontains']
    filter_fields = ['name__icontains','description__icontains']
    search_query_name = 'search'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subtitle"] = _('All flows')
        return context
    

class MyOrgListView(RTMBaseListView):
    template_name = 'flowhub/index.html'
    #permission = 'flohub.flow_list'
    model = Flow
    context_object_name = 'flows'
    search_fields = ['name__icontains','description__icontains']

    def get_queryset(self):
        return super().get_queryset().filter(org=self.request.org)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subtitle"] = "{} {}".format(self.request.org.name, _('flows'))
        return context   


class CreateView(SmartTemplateView):
    template_name = 'flowhub/form.html'
    success_url = reverse_lazy("flowhub.flow_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subtitle"] = _("Upload New Flow")
        context["form"] = FlowForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form  = FlowForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(self.request)
            messages.success(request, _('Flow created with success!'))
            return redirect(reverse('flowhub.flow_list'))
        else:
            context = self.get_context_data()
            context['form'] = form
            messages.error(request, _("Sorry, you did not complete the registration."))
            messages.error(request, form.non_field_errors())
            return render(request, self.template_name, context)


class EditView(SmartTemplateView):
    template_name = 'flowhub/form.html'
    #permission = "flowhub.flow_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flow = get_object_or_404(Flow, pk=self.kwargs["flow"])
        data = {
            "name": flow.name,
            "languages": flow.languages,
            "description": flow.description,
            "collected_data": flow.collected_data,
            "tags": list(flow.tags.values_list("name", flat=True)),
            "sdgs": flow.sdgs,
            "visible_globally": flow.visible_globally,
        }

        context["form"] = FlowForm(data=data, flow_is_required=False)
        context["page_subtitle"] = _("Edit")
        return context

    def post(self, request, *args, **kwargs):
        flow = get_object_or_404(Flow, pk=self.kwargs["flow"])
        form = FlowForm(request.POST, request.FILES, instance=flow, flow_is_required=False)

        if form.is_valid():
            instance = form.save(self.request)
            messages.success(request, _("Flow updated with success!"))
            return redirect(reverse("flowhub.flow_list"))
        else:
            context = self.get_context_data()
            context["form"] = form
            messages.error(request, _("Sorry, you did not complete the registration."))
            messages.error(request, form.non_field_errors())
            return render(request, self.template_name, context)


class DownloadView(SmartTemplateView):
    template_name = "flowhub/info.html"
    #permission = "flowhub.flow_info"

    def get(self, request, *args, **kwargs):
        super().get_context_data(**kwargs)
        flow = (
            Flow.objects.filter(pk=self.kwargs["flow"], is_active=True)
            .filter(Q(org=self.request.org) | Q(visible_globally=True))
            .first()
        )

        if not flow:
            return redirect(reverse("flowhub.flow_list"))

        response = HttpResponse(json.dumps(flow.flow), content_type="application/json")
        response["Content-Disposition"] = "attachment; filename=flow-{}.json".format(flow.pk)

        flow.increase_downloads()

        return response


class DeleteView(SmartTemplateView):
    template_name = 'flowhub/info.html'
    #permission = 'flowhub.flow_info'

    def post(self, request, *args, **kwargs):
        super().get_context_data(**kwargs)

        try:
            flow = Flow.objects.get(
                pk=kwargs.get('flow'),
                is_active = True,
                org = request.org
            )
        except Flow.DoesNotExist:
            flow = None
        
        if not Flow: return redirect(reverse('flowhub.flow_list'))

        flow.is_active = False
        flow.save()
        return redirect(self.request.META.get('HTTP_REFERER'))
