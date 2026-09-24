
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Word, Game, Guess
@login_required
def game(request):

    if 'game_id' not in request.session:
        word = Word.objects.order_by('?').first()

        game = Game.objects.create(
            user=request.user,
            word=word
        )

        request.session['game_id'] = game.id

    else:
        game = Game.objects.get(
            id=request.session['game_id']
        )

    result = []

    if request.method == 'POST':
        guess = request.POST['guess'].upper()

        guess_count = Guess.objects.filter(game=game).count()

        if guess_count < 5 and not game.completed:

            Guess.objects.create(
                game=game,
                guess=guess,
                guess_number=guess_count + 1
            )

            target = game.word.word

            for i in range(5):
                if guess[i] == target[i]:
                    result.append('green')
                elif guess[i] in target:
                    result.append('orange')
                else:
                    result.append('grey')

            print(result)

            if guess == target:
                game.won = True
                game.completed = True
                game.save()

            elif guess_count + 1 == 5:
                game.completed = True
                game.save()

    return render(request, 'game.html', {
        'game': game,
        'result': result
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect('game')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('game')

        return render(request, 'login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('login')