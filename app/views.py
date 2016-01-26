from app import app
from flask import render_template, flash, redirect
from .forms import RollForm
import random

@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to the Star Wars Dice Roller! Go to /roll to start!'

BoostResult = ['b0', 'b0', 'b1s', 'b1s1a', 'b2a', 'b1a']
SetbackResult = ['s0', 's0', 's1f', 's1f', 's1t', 's1t']
AbilityResult = ['a0', 'a1s', 'a1s', 'a2s', 'a1a', 'a1a', 'a1s1a', 'a2a']
DifficultyResult = ['d0', 'd1f', 'd2f', 'd1t', 'd1t', 'd1t', 'd2t', 'd1f1t']
ProfResult = ['p0', 'p1s', 'p1s', 'p2s', 'p2s', 'p1a', 'p1s1a', 'p1s1a', 'p1s1a', 'p2a', 'p2a', 'p1c']
ChallengeResult = ['c0', 'c1f', 'c1f', 'c2f', 'c2f', 'c1t', 'c1t', 'c1f1t', 'c1f1t', 'c2t', 'c2t', 'c1d']
ForceResult = ['f1b', 'f1b', 'f1b', 'f1b', 'f1b', 'f1b', 'f2b', 'f1w', 'f1w', 'f2w', 'f2w', 'f2w']

@app.route('/roll', methods=['GET', 'POST'])
def roll():
    form = RollForm()
    result = []
    if form.validate_on_submit():
        # Boost Dice:
        if form.boost.data:
            for i in range(form.boost.data):
                result.append(random.choice(BoostResult))
        if form.setback.data:
            for i in range(form.setback.data):
                result.append(random.choice(SetbackResult))
        if form.ability.data:
            for i in range(form.ability.data):
                result.append(random.choice(AbilityResult))
        if form.difficulty.data:
            for i in range(form.difficulty.data):
                result.append(random.choice(DifficultyResult))
        if form.prof.data:
            for i in range(form.prof.data):
                result.append(random.choice(ProfResult))
        if form.challenge.data:
            for i in range(form.challenge.data):
                result.append(random.choice(ChallengeResult))
        if form.force.data:
            for i in range(form.force.data):
                result.append(random.choice(ForceResult))
        return render_template('roll.html', form=RollForm(), result=result)
    return render_template('roll.html', form=form, result=result)
