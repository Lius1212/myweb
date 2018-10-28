import datetime
from django.contrib.contenttypes.fields import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from blog.models import Blog


def read_once_time(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        readnum, creared = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        date = timezone.now().date()
        readdetail, creared = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readdetail.read_num += 1
        readdetail.save()
    return key


def today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]


def week_hot_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lte=today,
                                read_details__date__gte=date).values('id', 'title').annotate(
                                read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]


def month_hot_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    blogs = Blog.objects.filter(read_details__date__lte=today,
                                read_details__date__gte=date).values('id', 'title').annotate(
        read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]


