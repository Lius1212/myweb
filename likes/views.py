from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount, LikeRecord, OpposeRecord, OpposeCount


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'status': 'ERROR', 'code': 401, 'msg': 'you were not login'})

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'ERROR', 'msg': 'object not exist'})

    if request.GET.get('is_like') == 'false':
        # oppose before
        if OpposeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            return JsonResponse({'status': 'ERROR', 'code': 405, 'msg': '你已经反对过了QAQ'})
        # don't like before
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                                user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.likes_num += 1
            like_count.save()
            return JsonResponse({'status': 'SUCCESS', 'likes_num': like_count.likes_num})
        else:
            return JsonResponse({'status': 'ERROR', 'msg': 'data error'})

    elif request.GET.get('is_like') == 'true':
        try:
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count = LikeCount.objects.get(content_type=content_type, object_id=object_id)
            like_count.likes_num -= 1
            like_count.save()
            return JsonResponse({'status': 'SUCCESS', 'likes_num': like_count.likes_num})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'ERROR', 'msg': 'object not exist'})

    else:
        return JsonResponse({'status': 'ERROR', 'msg': 'submit error'})


def oppose_change(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'status': 'ERROR', 'code': 401, 'msg': 'you were not login'})

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'ERROR', 'msg': 'object not exist'})

    if request.GET.get('is_oppose') == 'false':
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            return JsonResponse({'status': 'ERROR', 'code': 405, 'msg': '你已经支持过了QAQ'})

        oppose_record, created = OpposeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                                    user=user)
        if created:
            oppose_count, created = OpposeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            oppose_count.opposes_num += 1
            oppose_count.save()
            return JsonResponse({'status': 'SUCCESS', 'opposes_num': oppose_count.opposes_num})
        else:
            return JsonResponse({'status': 'ERROR', 'msg': 'data error'})

    elif request.GET.get('is_oppose') == 'true':
        try:
            oppose_record = OpposeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            oppose_record.delete()
            oppose_count = OpposeCount.objects.get(content_type=content_type, object_id=object_id)
            oppose_count.opposes_num -= 1
            oppose_count.save()
            return JsonResponse({'status': 'SUCCESS', 'opposes_num': oppose_count.opposes_num})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'ERROR', 'msg': 'object not exist'})

    else:
        return JsonResponse({'status': 'ERROR', 'msg': 'submit error'})
