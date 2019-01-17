from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.models import User
from read_record.utils import read_once_time
from .models import Blog, BlogType


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    previous_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    next_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()

    context = {}
    context['previous_blog'] = previous_blog
    context['next_blog'] = next_blog
    context['blog'] = blog
    response = render(request, 'blog/blog_detail.html', context)
    # Set and judge
    response.set_cookie(read_once_time(request, blog), 'true', max_age=600)
    return response


def get_blog_list_common(request, blog_all_list):
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_NUMBER)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1),
                            current_page_num)) + list(range(current_page_num,
                                                            min(current_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blog_all_list'] = blog_all_list
    context['blog_types'] = BlogType.objects.all().annotate(blog_count=Count('blog'))
    context['blog_authors'] = User.objects.all().annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    return context


def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common(request, blog_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common(request, blog_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_author(request, author_pk):
    author = get_object_or_404(User, pk=author_pk)
    blog_all_list = Blog.objects.filter(author=author)
    context = get_blog_list_common(request, blog_all_list)
    context['author'] = author
    return render(request, 'blog/blog_with_author.html', context)


def blog_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common(request, blog_all_list)
    context['blogs_with_date'] = '{0}年{1}月'.format(year, month)
    return render(request, 'blog/blog_with_date.html', context)


def blog_search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '').strip()
        blog_all_list = Blog.objects.filter(title__contains=keyword)
        context = get_blog_list_common(request, blog_all_list)
        context['keyword'] = keyword
        return render(request, 'blog/blog_search.html', context)
    else:
        return redirect(request.GET.get('from', reverse('home')))
