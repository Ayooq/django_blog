from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Post, Tag
from .utils import (
    search_query, pagination,
    ObjectCreateMixin, ObjectDetailMixin, ObjectUpdateMixin, ObjectDeleteMixin,
)
from .forms import PostForm, TagForm


def posts_list(request):
    posts = search_query(request, Post).filter(pub_date__lte=timezone.now())
    context = pagination(request, posts, 3)
    return render(request, 'blog/index.html', context=context)


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags/tags_list.html', context={'tags': tags})


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/posts/post_create.html'
    raise_exception = True


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tags/tag_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    form_model = PostForm
    template = 'blog/posts/post_update.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    form_model = TagForm
    template = 'blog/tags/tag_update.html'
    raise_exception = True


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/posts/post_detail.html'

    def get_queryset(self):
        """
        Исключает посты, запланированные к публикации в будущем.
        """
        return Post.objects.filter(pub_date__lte=timezone.now())


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tags/tag_detail.html'


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/posts/post_delete.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tags/tag_delete.html'
    raise_exception = True
