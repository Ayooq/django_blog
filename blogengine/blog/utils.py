from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Tag


def search_query(request, model):
    result = request.GET.get('search', '')

    if result:
        return model.objects.filter(
            Q(title__icontains=result) | Q(body__icontains=result)
        )
    else:
        return model.objects.all()


def pagination(request, items, per_page):
    paginator = Paginator(items, per_page)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    return {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(
            request, self.template, context={
                'obj': obj,
                'detail': True
            }
        )


class ObjectUpdateMixin:
    model = None
    form_model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(
            request, self.template, context={'obj': obj}
        )

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.model.__name__.lower() + 's_list_url'))
