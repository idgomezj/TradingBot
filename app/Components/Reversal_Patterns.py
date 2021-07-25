reversal_patterns = {
    'CDL2CROWS': 'Two Crows',
    'CDL3BLACKCROWS': 'Three Black Crows',
    'CDL3INSIDE': 'Three Inside Up/Down',
    'CDL3LINESTRIKE': 'Three-Line Strike',
    'CDL3OUTSIDE': 'Three Outside Up/Down',
    'CDL3STARSINSOUTH': 'Three Stars In The South',
    'CDL3WHITESOLDIERS': 'Three Advancing White Soldiers',
    'CDLABANDONEDBABY': 'Abandoned Baby',
    'CDLADVANCEBLOCK': 'Advance Block',
    'CDLBELTHOLD': 'Belt-hold',
    'CDLGRAVESTONEDOJI': 'Gravestone Doji',
    'CDLHANGINGMAN': 'Hanging Man',
    'CDLHARAMI': 'Harami Pattern',
    'CDLHARAMICROSS': 'Harami Cross Pattern',
    'CDLHIGHWAVE': 'High-Wave Candle',
    'CDLHIKKAKE': 'Hikkake Pattern',
    'CDLHIKKAKEMOD': 'Modified Hikkake Pattern',
    'CDLHOMINGPIGEON': 'Homing Pigeon',
    'CDLINVERTEDHAMMER': 'Inverted Hammer',
    'CDLKICKING': 'Kicking',
    'CDLKICKINGBYLENGTH': 'Kicking - bull/bear determined by the longer marubozu',
    'CDLLADDERBOTTOM': 'Ladder Bottom',
    'CDLLONGLEGGEDDOJI': 'Long Legged Doji',
    'CDLMATCHINGLOW': 'Matching Low',
    'CDLMORNINGDOJISTAR': 'Morning Doji Star',
    'CDLMORNINGSTAR': 'Morning Star',
    'CDLPIERCING': 'Piercing Pattern',
    'CDLRISEFALL3METHODS': 'Rising/Falling Three Methods',
    'CDLSEPARATINGLINES': 'Separating Lines',
    'CDLSHOOTINGSTAR': 'Shooting Star',
    'CDLSTICKSANDWICH': 'Stick Sandwich',
    'CDLTAKURI': 'Takuri (Dragonfly Doji with very long lower shadow)',
    'CDLTRISTAR': 'Tristar Pattern',
    'CDLUPSIDEGAP2CROWS': 'Upside Gap Two Crows',
    'CDLXSIDEGAP3METHODS': 'Upside/Downside Gap Three Methods'
}


pattern_down = {
    'CDLSTALLEDPATTERN': 'Stalled Pattern',
    'CDLDARKCLOUDCOVER': 'Dark Cloud Cover',
    'CDLDOJISTAR': 'Doji Star',
    'CDLEVENINGSTAR': 'Evening Star',
    'CDLIDENTICAL3CROWS': 'Identical Three Crows',

}


pattern_up = {
    'CDLHAMMER': 'Hammer',
    'CDLSHORTLINE': 'Short Line Candle',
    'CDLUNIQUE3RIVER': 'Unique 3 River',
}

pattern_break_suport = {
    'CDLBREAKAWAY': 'Breakaway',
}

pattern_continuity = {
    'CDLGAPSIDESIDEWHITE': 'Up/Down-gap side-by-side white lines',
    'CDLINNECK': 'In-Neck Pattern',
    'CDLONNECK': 'On-Neck Pattern',
    'CDLMATHOLD': 'Mat Hold',
    'CDLTASUKIGAP': 'Tasuki Gap',
    'CDLTHRUSTING': 'Thrusting Pattern',
}
pattern_data = {
    'CDLCOUNTERATTACK': 'Counterattack',
}


"""+200 bullish pattern with confirmation
+100 bullish pattern (most cases)
0 none
-100 bearish pattern
-200 bearish pattern with confirmation

for example
in case of CDLHIKKAKE pattern detection function:
as you can see in the source:

https://sourceforge.net/p/ta-lib/code/HEAD/tree/trunk/ta-lib/c/src/ta_func/ta_CDLHIKKAKE.c#l240

you can get one more -100 or +100 (that makes it -200/+200):
if your pattern have confirmation.
so the calculation will be (pattern+confirmation)
in that way,
you can potentially detect bearish pattern on some days, and one more day that confirm the pattern. and for the end get -200"""
