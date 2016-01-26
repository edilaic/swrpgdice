from flask.ext.wtf import Form
from wtforms.validators import Optional
from wtforms import IntegerField, TextField

class RollForm(Form):
    player = TextField('player')
    boost = IntegerField('boost', validators=[ Optional() ])
    ability = IntegerField('ability', validators=[ Optional() ])
    prof = IntegerField('prof', validators=[ Optional() ])
    setback = IntegerField('setback', validators=[ Optional() ])
    difficulty = IntegerField('difficulty', validators=[ Optional() ])
    challenge = IntegerField('challenge', validators=[ Optional() ])
    force = IntegerField('force', validators=[ Optional() ])
    percentile = IntegerField('percentile', validators=[ Optional() ])
