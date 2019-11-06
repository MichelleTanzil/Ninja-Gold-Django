from django.shortcuts import render, redirect
import random
from datetime import datetime
from django.urls import reverse


def index(request):
    if 'activities' not in request.session:
        request.session['activities'] = []
    if 'gold_amt' not in request.session:
        request.session['gold_amt'] = 0
    if 'display' not in request.session:
        request.session['display'] = 'none'
    if 'display_goal' not in request.session:
        request.session['display_goal'] = "block"
    if 'gold_goal' not in request.session:
        request.session['gold_goal'] = 500
    if 'move_goal' not in request.session:
        request.session['move_goal'] = 15
    return render(request, 'first_app/index.html')


def process_money(request, location):
    dt_string = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    gold_generator = {
        'farm': random.randint(10, 20),
        'cave': random.randint(5, 10),
        'house': random.randint(2, 5),
        'casino': random.randint(-50, 50),
    }
    request.session['move_goal'] -= 1
    if request.session['move_goal'] == 0 or request.session['gold_amt'] >= request.session['gold_goal']:
        request.session['display'] = 'inline-block'
        if request.session['gold_amt'] < request.session['gold_goal']:
            request.session['activities'].append("<p style='color: red'>You lose! Reset to try again!</p>")
        else: 
            request.session['activities'].append("<p style='color: green'>You Win! Reset to play again!</p>")
    elif request.session['move_goal'] < 0:
        request.session['move_goal'] = 0
        request.session['activities'].append("<p style='color: red'>That's all the moves you have, reset to play again!</p>")

    if request.session['move_goal'] > 0:
        request.session['gold_amt'] += gold_generator[location]

    if gold_generator[location] < 0 and request.session['move_goal'] > 0:
        request.session['activities'].append(f"<p style='color: red'> Earned {gold_generator[location]} from the {location}! ({dt_string}) </p>")
    elif gold_generator[location] > 0 and request.session['move_goal'] > 0:
        request.session['activities'].append(f"<p style='color: green'> Earned {gold_generator[location]} from the {location}! ({dt_string}) </p>")

    return redirect('/')

def win_conditions(request):
    request.session['display_goal'] = "none"
    request.session['gold_goal'] = int(request.POST['gold_goal'])
    request.session['move_goal'] = int(request.POST['move_goal'])
    return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')
