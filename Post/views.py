from django.shortcuts import get_object_or_404, redirect, render
from .models import Chatting, Posting
from User.models import User
from django.core.paginator import Paginator
from .forms import PostForm
# Create your views here.
def show(request):
    filter = request.GET.get('filter','')
    search = request.GET.get('search','')
    post_list = Posting.objects.all()
    if filter:
        if(filter=='vision'):
            post_list = post_list.filter(visualhearing=0)
        elif(filter=='hearing'):
            post_list = post_list.filter(visualhearing=1)
    if search:
            post_list = post_list.filter(title__contains=search)

    now_page =int(request.GET.get('page', 1))
    post_list = post_list.order_by('-post_idx')
                # 포스트 , 보여줄 게시글 개수
    p = Paginator(post_list, 10)
    info = p.get_page(now_page)

    # start_page = (now_page - 1) // 3 * 3 + 1
    # end_page = start_page + 3
    # if end_page > p.num_pages:
    #     end_page = p.num_pages

    # 페이지 마지막 번호
    last_page_num = 0
    for last_page in p.page_range:
        last_page_num = last_page 



    context = {
        'info' : info,
        'now_page' : now_page,
        'last_page_num' : last_page_num
    }
    print(info[0].date)
    return render(request, '../templates/post.html', context)


def form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            posting = form.save(commit=False)
            user = User.objects.get(username = request.session['username'])
            posting.id = user
            posting.save()
            return redirect('/post/')
    else:
        form = PostForm()

    return render(
        request, '../templates/post_posting.html', {'form' : form}
    )


def edit(request, pk):
    posting = Posting.objects.get(post_idx = pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=posting)
        if form.is_valid():
            posting.save()
            return redirect('/post/'+str(pk)+'/')
    else:
        form = PostForm(instance=posting)

    return render(
            request, '../templates/post_editing.html', {'form':form, 'pk' : pk}
        )


def detail(request, pk):
    result = get_object_or_404(Posting, post_idx = pk)
    user = User.objects.get(username = result.id)
    if request.method == 'POST':
        comment = Chatting()
        comment.username = request.session['username']
        comment.chatting = request.POST['body']
        comment.post_idx = Posting.objects.get(post_idx = pk)
        comment.save()

    comments = Chatting.objects.filter(post_idx = pk)
    context = {
        'result' : result, 
        'user' : user, 
        'comments' : comments, 
        }    
    print(type(result.id))
    print(type(user.username))
    print(type(request.session['username']))
    return render(request, '../templates/post_detail.html', context)





def delete(request, pk):
    post = Posting.objects.get(post_idx = pk)
    post.delete()
    return redirect('/post/')