#!/usr/bin/env python3 

"""This is the response module, it takes the outputs of classifier_tree as inputs, i.e: the
RECOGNIZED EVENTS. And it throws a response (or not) acording to the elapsed time of that EVENTS.

The time for events is managed whithin the 'VirtualClock' class

And the execution of rules based on events combination within the 'ResponseClass' class"""

from datetime import datetime
import random as rd

# Handle definitions and important methods of events
class EnvironmentEvents():
    def __init__(self):
        # Dict that list the possible environment events with their respective class
        # NON_MECHANIC:1, MECHANIC:2, TRANSPORTATION:3, BIOLOGICAL:4, GEOPHYSICAL:5
        self.event_dict = { 'HUMAN_CROWDS+CHILDREN+FOOTSTEPS':1, 'COMEDY+FANTASY+HUMOR':1, 'BABIES':1,
               'SCHOOLS&CROWDS':1, 'SPORT&LEISURE':1, 'HOSPITALS':1, 'HOUSEHOLD':2, 'INTERIOR_BACKGROUNDS':2,
               'COMMUNICATIONS':2, 'INDUSTRY':2, 'CITIES':2, 'FARM_MACHINERY':2, 'BUILDING':2,
               'TRANSPORT':3, 'CARS':3, 'SHIPS&BOATS':3, 'AIRCRAFT':3, 'TRAINS':3, 
               'ANIMALS&BIRDS':4, 'HORSES':4, 'DOMESTIC':4, 'WEATHER':5, 'WATER':5 }
        self.eventKeys = tuple(self.event_dict.keys())  # Lista de posibles eventos
    
    # Return every 'key' that has an specific value (eventKey)
    def get_kind(self, eventKey):
        return_keys = []
        for key, value in self.event_dict.items():
            if value == eventKey:
                return_keys.append(key)
        return return_keys
    
    def get_nonmechanic_keys(self):
        return self.get_kind(1)
    
    def get_mechanic_keys(self):
        return self.get_kind(2)
    
    def get_tranportation_keys(self):
        return self.get_kind(3)
    
    def get_biological_keys(self):
        return self.get_kind(4)
    
    def get_geophysical_keys(self):
        return self.get_kind(5)
    

# Handle everything related to events time values over time
class VirtualClock:
    def __init__(self, eventKeys):
        # Dict that handle the time (in seconds) for each type of event
        # It works like a counter of elapsed seconds for each event
        self.time_per_event = dict.fromkeys(eventKeys, 0)

    # Increments the elapsed time of an event (in seconds) by adding it 'incrementTime'
    # If and only if that event exist
    def increment_event(self, name_of_event, incrementTime):
        if self.time_per_event.get(name_of_event, None) != None:
            self.time_per_event[name_of_event] += incrementTime
    
    def decrement_event(self, name_of_event, decrementTime):
        if self.time_per_event.get(name_of_event, None) != None:
            self.time_per_event[name_of_event] -= decrementTime

    # Restart the elapsed time of an event (make it zero)
    def restart_event(self, name_of_event):
        if self.time_per_event.get(name_of_event, None) != None:  # Si el evento existe en el diccionario
            self.time_per_event[name_of_event] = 0
    


class ResponseClass:
    def __init__(self):
        self.events = EnvironmentEvents()
        self.vclock = VirtualClock(self.events.eventKeys)
    
    # Return True if elapsed time for a type of event is greather than specified_time
    # specified_time: Time to be validated. i.e. Example: if that event has been going on for two minutes
    # event_class: Class to be validated. Example:  non_mechanic=1, transportation=3,, etc.
    def isevent_triggered(self, specified_time, event_class, time_per_event, restart=False):
        # print(time_per_event)
        if event_class == 1:  # NonMechanic
            for curr_event in self.events.get_nonmechanic_keys():  # Traverse every NonMechanic event
                # Check if time of that event > specified time and return true if that happens
                if time_per_event.get(curr_event) > specified_time:
                    if restart: self.vclock.restart_event(curr_event)  # Restart current event's time (make it 0)
                    return True
        elif event_class == 2:  # Mechanic
            for curr_event in self.events.get_mechanic_keys():
                if time_per_event.get(curr_event) > specified_time:
                    if restart: self.vclock.restart_event(curr_event)
                    return True
        elif event_class == 3:  # Transportation
            for curr_event in self.events.get_tranportation_keys():
                if time_per_event.get(curr_event) > specified_time:  
                    if restart: self.vclock.restart_event(curr_event)
                    return True
        elif event_class == 4:  # Biological
            for curr_event in self.events.get_biological_keys():
                if time_per_event.get(curr_event) > specified_time:  
                    if restart: self.vclock.restart_event(curr_event)
                    return True
        elif event_class == 5:  # Geophysical
            for curr_event in self.events.get_geophysical_keys():
                if time_per_event.get(curr_event) > specified_time:  
                    if restart: self.vclock.restart_event(curr_event)
                    return True
        else:
            raise Exception("That rule doesn't exist yet")


    def calculate_response(self, time_per_event):        
        # Critical time of response module
        one_sec = 1
        half_min = 30
        two_min = 120
        four_min = 240
        #print(time_per_event)
        # Rule #1: Alert for NonMechanic events
        if self.isevent_triggered(two_min, 1, time_per_event, True):        
            print('WARNING SIGNAL TO PERSON/AUTHORITY IN CHARGE (Rule 1)')
            
        # Rule #2: Alert for Mechanic events
        if self.isevent_triggered(four_min, 2, time_per_event, True):
            print('WARNING SIGNAL TO PERSON/AUTHORITY IN CHARGE (Rule 2)')
        
        # Rule #3: Alert for Transportation events
        if self.isevent_triggered(four_min, 3, time_per_event, True):
            print('WARNING SIGNAL TO PERSON/AUTHORITY IN CHARGE (Rule 3)')
        
        # Rule #4: Alert for Mechanic+Biological events
        if self.isevent_triggered(one_sec, 2, time_per_event) and self.isevent_triggered(one_sec, 4, time_per_event):
            print('GENERATION OF AN ACOUSTIC SIGNAL IN INFRASOUND AND ULTRASOUND FRECUENCIES (Rule 4)')
        
        # Rule #5: Alert for NonMechanic+Mechanic events
        if self.isevent_triggered(four_min, 1, time_per_event) and self.isevent_triggered(four_min, 2, time_per_event):
            print('Supervision required (Rule 5)')
        
        # Rule #6: Alert for NonMechanical+Transportation events
        if self.isevent_triggered(half_min, 1, time_per_event) and self.isevent_triggered(half_min, 3, time_per_event):
            print('Warning signal to parents/person/authority in charge (imperative if children/babies) (Rule 6)')
        
        # Rule #7: Alert for Transportation+Geophysical events
        if self.isevent_triggered(one_sec, 3, time_per_event) and self.isevent_triggered(one_sec, 5, time_per_event):
            print('Warning signal about weather conditions on the road (Rule 7)')
        
        # Rule #8: Alert for NonMechanic+Biological events
        if self.isevent_triggered(two_min, 1, time_per_event) and self.isevent_triggered(two_min, 4, time_per_event):
            print('Supervision required (Rule 8)')
        
        # Rule #9: Alert for Mechanic+Geophysical events
        if self.isevent_triggered(one_sec, 2, time_per_event) and self.isevent_triggered(one_sec, 5, time_per_event):
            print('Supervision required (Rule 9)')
        
        # Rule #10: Alert for NonMechanic+Geophysical events
        if self.isevent_triggered(one_sec, 1, time_per_event) and self.isevent_triggered(one_sec, 5, time_per_event):
            print('Warning signal about weather conditions (Rule 10)')
        
    
    def run_simulation(self, iterations):
        """Simulate sounds for the number of iterations passed in the argument"""
        # a is the min value and b is the max value that can be randomly increased
        a = 2
        b = 20

        # Initialize all values of 'time_per_event' with 0, if they're not 0
        if any(self.vclock.time_per_event.values()):
            for i in self.vclock.time_per_event:
                self.vclock.time_per_event[i] = 0
        
        # Feed the random seed
        rd.seed(datetime.now())
        
        # Simulate sounds and store the duration (time elapsed) of each one
        # incrementing the time of that event by a certain value
        for i in range(iterations):
            for curr_event in self.events.get_nonmechanic_keys():
                self.vclock.increment_event(curr_event, rd.randrange(a, b))        
            for curr_event in self.events.get_mechanic_keys():
                self.vclock.increment_event(curr_event, rd.randrange(a, b))
            for curr_event in self.events.get_tranportation_keys():
                self.vclock.increment_event(curr_event, rd.randrange(a, b))        
            for curr_event in self.events.get_biological_keys():
                self.vclock.increment_event(curr_event, rd.randrange(a, b))        
            for curr_event in self.events.get_geophysical_keys():
                self.vclock.increment_event(curr_event, rd.randrange(a, b))

            # Call 'calculate_response' method few times to get 'notifications' or 'alarms'
            self.calculate_response(self.vclock.time_per_event)


# Initialize random seed and create ResponseClass object
# rmodule = ResponseClass()
# rmodule.run_simulation(100)
