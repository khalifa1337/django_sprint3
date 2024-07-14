from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post
from core.constants import ELEMENTS_TO_SHOW

def index(request):
    """Функция для отображения главной страницы."""
    template = 'blog/index.html'
    post_list = Post.published.all()[:ELEMENTS_TO_SHOW]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    """Функция для отображения страницы с содержимым поста."""
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.published,
        pk=post_id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Функция для отображения страницы с категорией."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )

    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__slug=category.slug
    )
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
