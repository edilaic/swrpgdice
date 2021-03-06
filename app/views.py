from flask import render_template, request, flash, redirect
from .forms import RollForm
import random
from flask_socketio import emit
from . import app, socketio
import json
import collections


BoostResult = ["b0", "b0", "b1s", "b1s1a", "b2a", "b1a"]
SetbackResult = ["s0", "s0", "s1f", "s1f", "s1t", "s1t"]
AbilityResult = ["a0", "a1s", "a1s", "a2s", "a1a", "a1a", "a1s1a", "a2a"]
DifficultyResult = ["d0", "d1f", "d2f", "d1t", "d1t", "d1t", "d2t", "d1f1t"]
ProfResult = ["p0", "p1s", "p1s", "p2s", "p2s", "p1a", "p1s1a", "p1s1a", "p1s1a", "p2a", "p2a", "p1c"]
ChallengeResult = ["c0", "c1f", "c1f", "c2f", "c2f", "c1t", "c1t", "c1f1t", "c1f1t", "c2t", "c2t", "c1d"]
ForceResult = ["f1b", "f1b", "f1b", "f1b", "f1b", "f1b", "f2b", "f1w", "f1w", "f2w", "f2w", "f2w"]
prevRolls = collections.deque([], 5)
destinyDice = {'light': 0, 'dark': 0}

# Initiative Variables
initorder = []
round = 1
initposition = 0

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
        retval = retval + str(netsuccess)
        if netsuccess > 1:
            retval = retval + " Successes "
        else:
            retval = retval + " Success "
        retval = retval + "<span class='eotesymbols'>s</span> "
    elif netsuccess < 0:
        retval = retval + str(-netsuccess)
        if -netsuccess > 1:
            retval = retval + " Failures "
        else:
            retval = retval + " Failure "
        retval = retval + "<span class='eotesymbols'>f</span> "
    if netadvantage > 0:
        retval = retval + str(netadvantage)
        if netadvantage > 1:
            retval = retval + " Advantages "
        else:
            retval = retval + " Advantage "
        retval = retval + "<span class='eotesymbols'>a</span> "
    elif netadvantage < 0:
        retval = retval + str(-netadvantage)
        if -netadvantage > 1:
            retval = retval + " Threats "
        else:
            retval = retval + " Threat "
        retval = retval + "<span class='eotesymbols'>t</span> "
    if despairs > 0:
        retval = retval + str(despairs)
        if despairs > 1:
            retval = retval + " Despairs "
        else:
            retval = retval + " Despair "
        retval = retval + "<span class='eotesymbols'>y</span> "
    if triumphs > 0:
        retval = retval + str(triumphs)
        if triumphs > 1:
            retval = retval + " Triumphs "
        else:
            retval = retval + " Triumph "
        retval = retval + "<span class='eotesymbols'>x</span> "
    return retval


@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to the Star Wars Dice Roller! Go to /roll to start!'


@app.route('/crawl')
def crawl():
    return render_template('crawl.html')


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
        prevRolls.append(data)
        socketio.emit('edroll', {'data': json.dumps(data)}, namespace='/swdice')
        return render_template('roll.html', form=RollForm(), result=result)
    return render_template('roll.html', form=form, result=result)


@app.route('/gm', methods=['GET', 'POST'])
def gm():
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
        prevRolls.append(data)
        socketio.emit('edroll', {'data': json.dumps(data)}, namespace='/swdice')
        return render_template('gm.html', form=RollForm(), result=result)
    return render_template('gm.html', form=form, result=result)


@app.route('/destiny', methods=['GET'])
def destiny():
    if request.args.get('side') and destinyDice[request.args.get('side')] > 0:
        if request.args.get('side') == 'light':
            destinyDice['light'] = destinyDice['light'] - 1
            destinyDice['dark'] = destinyDice['dark'] + 1
        else:
            destinyDice['light'] = destinyDice['light'] + 1
            destinyDice['dark'] = destinyDice['dark'] - 1
        result = " used a " + request.args.get('side') + " destiny point!"
        data = {'light': destinyDice['light'], 'dark': destinyDice['dark'], 'player': request.args.get('player'), 'change': result}
        socketio.emit('destiny', {'data': json.dumps(data)}, namespace='/swdice')
        return ''
    return ''


@app.route('/setdestiny', methods=['GET'])
def setdestiny():
    if request.args.get('dark') and request.args.get('light'):
        destinyDice['light'] = int(request.args.get('light'))
        destinyDice['dark'] = int(request.args.get('dark'))
        result = "The Destiny Pool has been set to " + request.args.get('light') + " light side points and " + request.args.get('dark') + " dark side points."
        data = {'light': destinyDice['light'], 'dark': destinyDice['dark'], 'change': result}
        socketio.emit('setdestiny', {'data': json.dumps(data)}, namespace='/swdice')
        return ''
    return ''


@app.route('/game')
def game():
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
        prevRolls.append(data)
        socketio.emit('edroll', {'data': json.dumps(data)}, namespace='/swdice')
    return render_template('game.html', form=RollForm(), result=result)


@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@socketio.on('initInit', namespace='/swdice')
def socket_initInit(data):
	global initorder, round, initposition
	initorder = data['initorder']
	round = data['round']
	initposition = data['initposition']
	socketio.emit('displayinit', {'data': json.dumps(data)}, namespace='/swdice')
	
@socketio.on('initReset', namespace='/swdice')
def socket_initReset():
	global initorder, round, initposition
	initorder = []
	round = 1
	initposition = 0
	socketio.emit('resetinitiative', namespace='/swdice')
	
@socketio.on('initNext', namespace='/swdice')
def socket_initNext():
	global round, initposition
	if initposition == ( len(initorder) - 1):
		initposition = 0
		round = round + 1
	else: 
		initposition = initposition + 1
	data = { 'round' : round, 'initposition' : initposition }
	socketio.emit('nextinitiative', {'data': json.dumps(data)}, namespace='/swdice')
	
@socketio.on('initBack', namespace='/swdice')
def socket_initBack():
	global round, initposition
	if initposition == 0:
		if round != 1:
			initposition = len(initorder) - 1
			round = round - 1
	else: 
		initposition = initposition - 1
	data = { 'round' : round, 'initposition' : initposition }
	socketio.emit('backinitiative', {'data': json.dumps(data)}, namespace='/swdice')

@socketio.on('connect', namespace='/swdice')
def socket_connect():
	data = { 'initorder': initorder, 'round' : round, 'initposition' : initposition }
	socketio.emit('displayinit', {'data': json.dumps(data)}, namespace='/swdice')
	for d in prevRolls:
		emit('edroll', {'data': json.dumps(d)}, namespace='/swdice')
	print ('Socket Connected!')


@socketio.on('disconnect', namespace='/swdice')
def socket_disconnect():
    print ('Socket Disconnected!')


@socketio.on_error_default
def default_error_handler(e):
	print('OMG an error! D:') # D:
	print(request.event["message"])  # "my error event"
	print(request.event["args"])     # (data,)
