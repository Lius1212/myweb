from django.shortcuts import render
from django.contrib.contenttypes.fields import ContentType
from django.db.models import Count
from blog.models import Blog, BlogType
from read_record.utils import today_hot_data, week_hot_data, month_hot_data


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)

    context = {}
    context['blog_nums'] = Blog.objects.all().count()
    context['today_hot_blog'] = today_hot_data(blog_content_type)
    context['week_hot_blog'] = week_hot_data()
    context['month_hot_blog'] = month_hot_data()
    context['blog_types_sequence'] = BlogType.objects.all().annotate(blog_count=Count('blog')).order_by('-blog_count')
    return render(request, 'home.html', context)
