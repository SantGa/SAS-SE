#!/usr/bin/env python3

"""This module manages is responsible for coordinating and executing
the autonomous cycle, it uses 'classifier_tree.py' and 'response_module.py'"""

import response_module as resmod
import Classifier.classifier_tree as classifier
import queue
import time
import random as rd
from datetime import datetime

rd.seed(datetime.now())

"""Convert events from numbers to their respecive names 
Ex: 0->'HUMAN_CROWDS+CHILDREN+FOOTSTEPS', 1->'COMEDY+FANTASY+HUMOR', 3->''SCHOOLS&CROWDS', etc
After that, it classifies it as the 'more general events' (NonMechanic, Mechanic, etc)"""
def convert_events(event_keys, num_of_event):  # Can be used for dashboard
    event_name = event_keys[num_of_event]
    return event_name

# Decrements one second
def decounter(vclock, event_dict):
    time_per_event = vclock.time_per_event

    for event, time in time_per_event.items():
        if time >= 1:
            #print("Decounter: ")
            vclock.decrement_event(event, 1)
            #print(time_per_event)
    #print(time_per_event)

def validator(triggered_events, vclock, validator_clock):
    validator_dict = validator_clock.time_per_event
    print("triggered events:", triggered_events)
    
    for name_of_event, value in validator_dict.items():
        validator_clock.increment_event(name_of_event,1)
        #print("entro", name_of_event, value)
        if value == 8:
            vclock.restart_event(name_of_event)
            validator_clock.restart_event(name_of_event)
            #print("reseteo!!", name_of_event)
    print("vclock: ", vclock.time_per_event.values())
    #print("paso1: ",validator_dict)

    for event in triggered_events:
        for name_of_event in validator_dict.keys():
            if name_of_event == event:
                validator_clock.restart_event(name_of_event)  # Event happened, reset    
    #print("Paso2: ",validator_dict)

            
def generate_events():
    num_of_events = rd.randrange(1,6)
    events = classifier.output_events_randomly(num_of_events)
    #print(events)
    return events
# Output a few events randomly

def simulate_autonomous_cycle(num_of_iterations):
    env_events = resmod.EnvironmentEvents()
    event_keys = env_events.eventKeys
    vclock = resmod.VirtualClock(event_keys)  # Used to track events time
    validator_clock = resmod.VirtualClock(event_keys)  # Used to reset events (of vclock) if they don't happen for some time
    time_per_event = vclock.time_per_event
    resp = resmod.ResponseClass()
    stop = num_of_iterations #Number of iterations 

    while True:
        events = generate_events()
        triggered_events = []
        for event in events:
            name_of_event = convert_events(event_keys, event[0])  # Search name by number
            vclock.increment_event(name_of_event, event[1])  # Increment time value of that event
            triggered_events.append(name_of_event)

            #kind_of_event = env_events.event_dict[name_of_event]
            resp.calculate_response(time_per_event)
        time.sleep(1)  # Delay between events
        decounter(vclock, events)
        validator(triggered_events, vclock, validator_clock)

        if stop < 1:
            break
        else:
            stop -= 1

simulate_autonomous_cycle(50)
