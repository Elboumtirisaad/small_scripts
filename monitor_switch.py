import ahk
import itertools
import ast

total_height = ahk.total_height()
total_width = ahk.total_width()
monitors = ahk.monitor_count()
offset = total_width//monitors
start = offset//2
x1 = start
x2 = start + offset
y = total_height//2
rx1 = x1
ry1 = y
rx2 = x2
ry1 = y
count = False
bank = 0
filename = "locdata.txt"

slots = [{"range":[0], "padding":1,
          "numrepetitions":1, "delay":1,
          "buttons":["L"]} for _ in range(10)]

locations = [[0,0] for _ in range(100)]

data = {'locations':locations, 'slots':slots, 'interrupted':False}

ahk.bind("<shift-pause>", ahk.mouse_move, x1, y)
ahk.bind("<alt-pause>", ahk.mouse_move, x2, y)

def parse_range(s):
    # parse_range('1, 2, 5-9, 2, 8-5') returns
    # [1, 2, 5, 6, 7, 8, 9, 2, 8, 7, 6, 5]
    result = []
    for part in s.split(','):
        if '-' in part:
            a,b = map(int, part.split('-'))
            if a<=b:
                step = 1
            else:
                step = -1
            result.extend(range(a, b+step, step))
        else:
            result.append(int(part))
    return result
    
def expand_sequence(r, seq):
    # expand_sequence([1, 4, 9], 'L R') returns ['L', 'R', 'L']
    return list(zip(*zip(r, itertools.cycle(seq.split()))))[1]

def save():
    with open(filename, 'w') as output:
        output.write(repr(locations))
        output.write('\n')
        output.write(repr(slots))

def load():
    with open(filename) as f:
        data['locations'] = ast.literal_eval(next(f))
        data['slots'] = ast.literal_eval(next(f))
    
def create_cycle():
    slot = ahk.inputbox('Save/load/cancel', 'Save this in slot 1-10, cancel, save data (SAVE), or load data (LOAD)?')
    if slot == 'SAVE':
        save()
        return
    if slot == 'LOAD':
        load()
        return
    if not 1 <= slot <= 10:
        return
    rng = parse_range(ahk.inputbox('Numbers', 'Enter a range of locations e.g. "1`, 2`, 5-9`, 2", 8-5'))
    padding = ahk.inputbox('Padding time', 'How many seconds padding around clicks (decimal okay)?')
    numrepetitions = ahk.inputbox('Repetitions', 'How many times?')
    delay = ahk.inputbox('Delay', 'Pause how many seconds between cycles (decimal okay)?')
    buttons = ahk.inputbox('Button sequence',
        'Enter a mouse button sequence to repeat, like "L R R". L=Left, R=Right, M=Middle, X1=Button4, X2=Button5.')
    data['slots'][slot] = {"range":rng, "padding":padding, "numrepetitions":numrepetitions,
                           "delay":delay, "buttons":expand_sequence(rng, buttons)}

def do_slot(num):
    data['interrupted'] = False
    data['slots'][num]['numrepetitions'] = ahk.inputbox('Repetitions',
                                                        'How many times?',
                                                        default=data['slots'][num]['numrepetitions']
    for i in range(data['slots'][num]['numrepetitions']):
        for idx,r in enumerate(data['slots'][num]['range']):
            ahk.mousemove(*data['locations'][r])
            ahk.sleep(data['slots'][num]['padding'] * 500)
            if data['interrupted']:
                return
            ahk.click(data['slots'][num]['buttons'][idx]
            ahk.sleep(data['slots'][num]['padding'] * 500
        if i != data['slots'][num]['numrepetitions']:
            if data['interrupted']:
                return
            ahk.sleep(data['slots'][num]['delay'] * 1000)

    
    
    
    

    
    
    
    
    
    
    
    
    