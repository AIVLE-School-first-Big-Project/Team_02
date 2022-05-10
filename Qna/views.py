from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
from .models import Qna_Posting, Qna_Chatting
from User.models import User
from django.core.paginator import Paginator


def qna_post(request):
    qna_list = Qna_Posting.objects.all()
    now_page = int(request.GET.get('page', 1))
    qna_list = qna_list.order_by('-qna_idx')
    p = Paginator(qna_list, 10)
    info = p.get_page(now_page)

    last_page_num = 0
    for last_page in p.page_range:
        last_page_num = last_page

    context = {
        'info': info,
        'now_page': now_page,
        'last_page_num': last_page_num
    }
    return render(request, '../templates/qna.html', context)


def form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            qna_posting = form.save(commit=False)
            user = User.objects.get(username=request.session['username'])
            qna_posting.id = user
            qna_posting.save()
            return redirect('/qna/')
    else:
        form = PostForm()

    return render(
        request, '../templates/qna_posting.html', {'form': form}
    )


def qna_edit(request, pk):
    qna_posting = Qna_Posting.objects.get(qna_idx=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=qna_posting)
        if form.is_valid():
            qna_posting.save()
            return redirect('/qna/'+str(pk)+'/')
    else:
        form = PostForm(instance=qna_posting)

    return render(
            request, '../templates/qna_editing.html', {'form': form, 'pk': pk}
        )


def qna_detail(request, pk):
    result = get_object_or_404(Qna_Posting, qna_idx=pk)
    user = User.objects.get(username=result.id)

    if request.method == 'POST':
        comment = Qna_Chatting()
        comment.username = request.session['username']
        comment.chatting = request.POST['body']
        comment.qna_idx = Qna_Posting.objects.get(qna_idx=pk)
        comment.save()

    comments = Qna_Chatting.objects.filter(qna_idx=pk)
    context = {
        'result': result,
        'user': user,
        'comments': comments,
        }
    return render(request, '../templates/qna_detail.html', context)


def delete(request, pk):
    post = Qna_Posting.objects.get(qna_idx=pk)
    post.delete()
    return redirect('/qna/')
