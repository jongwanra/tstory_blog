from django.shortcuts import render

from .forms import RegisterForm


def register(request):
    # HTML form 태그에서 사용하는 POST방식
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            # commit을 하면, db에 저장이 안되고 메모리상에서만 저장됨
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()  # 여기서 db에 저장.
            return render(request, 'registration/login.html', {'user': user})
    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html', {'user_form': user_form})
