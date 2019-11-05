from django.shortcuts import render, redirect
import random
from datetime import datetime
from django.urls import reverse


def index(request):
    if 'activities' not in request.session:
        request.session['activities'] = []
    if 'gold_amt' not in request.session:
        request.session['gold_amt'] = 0
    if 'moves' not in request.session:
        request.session['moves'] = 15
    if 'display' not in request.session:
        request.session['display'] = 'none'
    return render(request, 'first_app/index.html')


def process_money(request):
    dt_string = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    gold_generator = {
        'farm': random.randint(10, 20),
        'cave': random.randint(5, 10),
        'house': random.randint(2, 5),
        'casino': random.randint(-50, 50),
    }
    request.session['moves'] -= 1
    if request.session['moves'] == 0 or request.session['gold_amt'] >= 500:
        request.session['display'] = 'inline-block'
        if request.session['gold_amt'] < 500:
            request.session['activities'].append("<p style='color: red'>You lose! Reset to try again!</p>")
        else: 
            request.session['activities'].append("<p style='color: green'>You Win! Reset to play again!</p>")
    elif request.session['moves'] < 0:
        request.session['moves'] = 0
        request.session['activities'].append("<p style='color: red'>That's all the moves you have, reset to play again!</p>")
    
    location = request.POST["location"]
    if request.session['moves'] > 0:
        request.session['gold_amt'] += gold_generator[location]

    if gold_generator[location] < 0 and request.session['moves'] > 0:
        request.session['activities'].append(f"<p style='color: red'> Earned {gold_generator[location]} from the {location}! ({dt_string}) </p>")
    elif gold_generator[location] > 0 and request.session['moves'] > 0:
        request.session['activities'].append(f"<p style='color: green'> Earned {gold_generator[location]} from the {location}! ({dt_string}) </p>")

    return redirect('/')


def reset(request):
    request.session.clear()
    return redirect('/')
