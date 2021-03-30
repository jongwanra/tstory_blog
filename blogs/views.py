# 가져오거나 없을 땐 404페이지를 표시하는 메소드
# 첫 번째 인자는 모델, 두 번쨰 인자는 키워드 만약 키워드가 없으면, 404에러 발생
# Example) q = get_object_or_404(Question, id=pk)
# 보통은 예외처리를 해주는데, 이 메소드 덕분에 편리하게 사용 가능

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from blogs.models import Comment, Post
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.


def posts_list(request):
    # 최신 순으로 객체 불러오기(기준: created_at)
    posts = Post.objects.order_by('-created_at')

    return render(request, 'blogs/posts_list.html', context={'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # comment 기능 추가(각 글마다 적혀있던 comment들만 가져옴)
    comments = Comment.objects.filter(post=post.id)
    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    return render(request, 'blogs/post_detail.html', context={'post': post, 'comments': comments, 'is_liked': is_liked, 'total_likes': post.total_likes()})


@login_required
@require_POST
def post_like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = post.likes.filter(id=request.user.id).exists()

    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))


@login_required  # login 했는지 여부를 체크해줌(Decorator)
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not content:
            errors.append('내용을 입력해주세요.')

        if not errors:
            post = Post.objects.create(
                user=request.user, title=title, content=content, image=image)

            # redirect는 함수뷰 이름을 적어주면 바로 그쪽으로 넘김
            # /post/%d/ % post.id == reverse('post_detail', args=['post.id': article.id])
            return redirect(reverse('post_detail', kwargs={'post_id': post.id}))

    return render(request, 'blogs/post_write.html', {'user': request.user, 'errors': errors})


@login_required
def comment_write(request):
    errors = []
    if request.method == 'POST':
        post_id = request.POST.get('post_id', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            errors.append('댓글을 입력해주세요.')

        if not errors:
            comment = Comment.objects.create(
                user=request.user, post_id=post_id, content=content)

        return redirect(reverse('post_detail', kwargs={'post_id': comment.post.id}))

    return render(request, 'blogs/post_detail.html', {'user': request.user, 'errors': errors})
