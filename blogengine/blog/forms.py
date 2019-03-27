from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Tag


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags', 'pub_date']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название поста'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес URL'
            }),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'pub_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Для отложенных записей'
            })
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError(
                'Этот путь уже занят! Введите что-то другое.'
            )
        return new_slug


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название тэга'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес URL'
            })
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create' or Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(
                'Этот путь уже занят! Введите что-то другое.'
            )
        return new_slug
