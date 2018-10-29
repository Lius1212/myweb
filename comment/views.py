from django.shortcuts import redirect, reverse
from .models import Comment
from .forms import CommentForm


def create_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.commentator = comment_form.cleaned_data['user']
        comment.content = comment_form.cleaned_data['content']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()

    return redirect(request.GET.get('from', reverse('home')))
