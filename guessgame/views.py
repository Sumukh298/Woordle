
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Word, Game, Guess
from django.utils import timezone
def check_guess(guess, target):
    result = ['grey'] * 5

    letter_count = {}

    for letter in target:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1

    # Pass 1: exact matches
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'green'
            letter_count[guess[i]] -= 1

    # Pass 2: misplaced letters
    for i in range(5):
        if result[i] == 'grey' and guess[i] in letter_count and letter_count[guess[i]] > 0:
            result[i] = 'orange'
            letter_count[guess[i]] -= 1

    return result

    
@login_required
def game(request):

    if 'game_id' not in request.session:

        games_today = Game.objects.filter(
            user=request.user,
            date=timezone.localdate()
        ).count()

        if games_today >= 3:
            return render(request, 'game.html', {
                'limit_reached': True
            })

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

        if len(guess) != 5:
            guesses = Guess.objects.filter(
                game=game
            ).order_by('guess_number')

            return render(request, 'game.html', {
                'game': game,
                'result': result,
                'guesses': guesses,
                'error': 'Guess must be exactly 5 letters.'
            })

        guess_count = Guess.objects.filter(game=game).count()

        if guess_count < 5 and not game.completed:

            Guess.objects.create(
                game=game,
                guess=guess,
                guess_number=guess_count + 1
            )

            target = game.word.word
            result = check_guess(guess, target)

            if guess == target:
                game.won = True
                game.completed = True
                game.save()

            elif guess_count + 1 == 5:
                game.completed = True
                game.save()

    guesses = Guess.objects.filter(
        game=game
    ).order_by('guess_number')
    guess_results = []

    for previous_guess in guesses:
        colors = check_guess(
            previous_guess.guess,
            game.word.word
        )

        tiles = []

        for i in range(5):
            tiles.append({
                'letter': previous_guess.guess[i],
                'color': colors[i]
            })

        guess_results.append({
            'tiles': tiles
        })

    return render(request, 'game.html', {
        'game': game,
        'result': result,
        'guesses': guess_results
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
#remove this after finsihing
@login_required
def reset_game(request):
    Game.objects.filter(
        user=request.user,
        date=timezone.localdate()
    ).delete()

    if 'game_id' in request.session:
        del request.session['game_id']

    return redirect('game')
@login_required
def next_game(request):
    if 'game_id' in request.session:
        del request.session['game_id']

    return redirect('game')
