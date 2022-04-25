from django.shortcuts import render
from .models import Qna_Posting, Qna_Chatting
from User.models import User
from django.core.paginator import Paginator
#from .forms import PostForm

def qna(request):
    qna_list = Qna_Posting.objects.all()
    now_page =int(request.GET.get('page', 1))
    qna_list = qna_list.order_by('-qna_idx')
                # 포스트 , 보여줄 게시글 개수
    p = Paginator(qna_list, 10)
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
    return render(request, '../templates/qna.html', context)


def qna_edit():
    return

def qna_detail():
    return