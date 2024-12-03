from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from pybo.models import Question

def index(req):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = req.GET.get('page', '1') # 페이지
    # 조회
    question_list = Question.objects.order_by('-create_date')
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 한 화면에 보여질 글의 개수
    page_obj = paginator.get_page(page)
    # templates/pybo/question_list.html : question_list 형태로 page_obj 를 전달
    # page_obj : 질문 글을 시간 역순을 정렬 + 한 화면에 10개만 보여줌 + paginator 로 페이징된 객체
    context = {'question_list': page_obj} 
    return render(req, "pybo/question_list.html", context)

def detail(req, question_id):
    """
    pybo 질문 내용 출력
    """
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}
    return render(req, 'pybo/question_detail.html', context)