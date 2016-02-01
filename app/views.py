from flask import render_template, request, flash, redirect
from .forms import RollForm
import random
from flask_socketio import emit
from . import app, socketio
import json


@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to the Star Wars Dice Roller! Go to /roll to start!'


@app.route('/crawl')
def crawl():
    return render_template('crawl.html')

BoostResult = ["b0", "b0", "b1s", "b1s1a", "b2a", "b1a"]
SetbackResult = ["s0", "s0", "s1f", "s1f", "s1t", "s1t"]
AbilityResult = ["a0", "a1s", "a1s", "a2s", "a1a", "a1a", "a1s1a", "a2a"]
DifficultyResult = ["d0", "d1f", "d2f", "d1t", "d1t", "d1t", "d2t", "d1f1t"]
ProfResult = ["p0", "p1s", "p1s", "p2s", "p2s", "p1a", "p1s1a", "p1s1a", "p1s1a", "p2a", "p2a", "p1c"]
ChallengeResult = ["c0", "c1f", "c1f", "c2f", "c2f", "c1t", "c1t", "c1f1t", "c1f1t", "c2t", "c2t", "c1d"]
ForceResult = ["f1b", "f1b", "f1b", "f1b", "f1b", "f1b", "f2b", "f1w", "f1w", "f2w", "f2w", "f2w"]

def parse_result(result):
    successes = 0
    advantages = 0
    failures = 0
    threats = 0
    despairs = 0
    triumphs = 0
    for r in result:
        value = r[1:]
        for p in (value[pos:pos + 2] for pos in xrange(0, len(value), 2)):
            if len(p) == 2:
                if p[1] == 's':
                    successes = successes + int(p[0])
                elif p[1] == 'a':
                    advantages = advantages + int(p[0])
                elif p[1] == 'f':
                    failures = failures + int(p[0])
                elif p[1] == 't':
                    threats = threats + int(p[0])
                elif p[1] == 'd':
                    despairs = despairs + int(p[0])
                elif p[1] == 'c':
                    triumphs = triumphs + int(p[0])
    netsuccess = successes - failures + triumphs - despairs
    netadvantage = advantages - threats
    retval = ""
    if netsuccess > 0:
        retval = retval + str(netsuccess) + " Success "
    elif netsuccess < 0:
        retval = retval + str(-netsuccess) + " Failure "
    if netadvantage > 0:
        retval = retval + str(netadvantage) + " Advantage "
    elif netadvantage < 0:
        retval = retval + str(-netadvantage) + " Threat "
    if despairs > 0:
        retval = retval + str(despairs) + " Despair "
    if triumphs > 0:
        retval = retval + str(triumphs) + " Triumph "
    return retval


@app.route('/roll', methods=['GET', 'POST'])
def roll():
    form = RollForm()
    result = []
    if form.validate_on_submit():
        # Boost Dice:
        player = form.player.data
        if form.boost.data:
            for i in range(form.boost.data):
                result.append(random.choice(BoostResult))
        if form.ability.data:
            for i in range(form.ability.data):
                result.append(random.choice(AbilityResult))
        if form.prof.data:
            for i in range(form.prof.data):
                result.append(random.choice(ProfResult))
        if form.setback.data:
            for i in range(form.setback.data):
                result.append(random.choice(SetbackResult))
        if form.difficulty.data:
            for i in range(form.difficulty.data):
                result.append(random.choice(DifficultyResult))
        if form.challenge.data:
            for i in range(form.challenge.data):
                result.append(random.choice(ChallengeResult))
        if form.force.data:
            for i in range(form.force.data):
                result.append(random.choice(ForceResult))
        data = {'dice': result, 'player': player, 'total': parse_result(result)}
        if form.percentile.data:
            for i in range(form.percentile.data):
                if data['total'] == '':
                    data['total'] = str(random.randint(0,99))
                else:
                    data['total'] = data['total'] + ' and ' + str(random.randint(0,99))
            data['total'] = data['total'] + ' on percentile'
        socketio.emit('edroll', {'data': json.dumps(data)}, namespace='/swdice')
        return render_template('roll.html', form=RollForm(), result=result)
    return render_template('roll.html', form=form, result=result)


@socketio.on('connect', namespace='/swdice')
def socket_connect():
    print ('Socket Connected!')


@socketio.on('disconnect', namespace='/swdice')
def socket_disconnect():
    print ('Socket Disconnected!')


@app.route('/monitor')
def monitor():
    print ('Loading monitor')
    return render_template('monitor.html')


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])     # (data,)
