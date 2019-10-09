from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _

from smartmin.views import SmartTemplateView
from dash.orgs.models import Org

from ureport.utils import get_paginator, log_save

from .forms import UnctForm


class ListView(SmartTemplateView):
    template_name = "uncts/index.html"
    permission = "uncts.unct_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        sort_field = self.request.GET.get("sort")
        sort_direction = self.request.GET.get("dir")
        page = self.request.GET.get("page")

        filters = {}
        sortered = "name"

        if query:
            filters["name__icontains"] = query

        if sort_field:
            sortered = "{}{}".format("-" if sort_direction == "desc" else "", sort_field)

        context["orgs"] = get_paginator(Org.objects.filter(**filters, is_active=True).order_by(sortered), page)
        context["query"] = query
        return context


class CreateView(SmartTemplateView):
    template_name = "uncts/form.html"
    permission = "uncts.unct_create"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UnctForm()
        context["page_subtitle"] = _("New")
        return context

    def post(self, request, *args, **kwargs):
        form = UnctForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(request.user)
            messages.success(request, _("UNCT created with success!"))
            log_save(self.request.user, instance, 1)
            return redirect(reverse("uncts.unct_list"))
        else:
            context = self.get_context_data()
            context["form"] = form
            messages.error(request, form.non_field_errors())
            messages.error(request, _("Sorry, you did not complete the registration."))
            return render(request, self.template_name, context)


class EditView(SmartTemplateView):
    template_name = "uncts/form.html"
    permission = "uncts.unct_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unct = get_object_or_404(Org, pk=self.kwargs["unct"])

        data = {
            "name": unct.name,
            "language": unct.language,
            "subdomain": unct.subdomain,
            "timezone": unct.timezone,
            "host": unct.backends.first().host,
            "api_token": unct.backends.first().api_token,
        }

        context["form"] = UnctForm(initial=data)
        context["page_subtitle"] = _("Edit {}".format(unct.name))
        return context

    def post(self, request, *args, **kwargs):
        unct = get_object_or_404(Org, pk=self.kwargs["unct"])
        form = UnctForm(request.POST, request.FILES, instance=unct)

        if form.is_valid():
            instance = form.save(request.user)
            messages.success(request, _("UNCT edited with success!"))
            log_save(self.request.user, instance, 2)
            return redirect(reverse("uncts.unct_list"))
        else:
            context = self.get_context_data()
            context["form"] = form
            messages.error(request, form.non_field_errors())
            messages.error(request, _("Sorry, you did not complete the registration."))
            return render(request, self.template_name, context)