#-*- encoding: utf-8 -*-

#import modes
import pygame

from log import Log
from log import Singleton

FASTRACE, CHAMPIONSHIP, TIMED = range(3)

class Config:
    __metaclass__ = Singleton
    def __init__(self):
        Log().info('Constructor: Config')
        self.player_selected = None
        self.mode = None
        self.competitors = []
        self.debug = False
        self.level_debug = 0
        self.championship = None
        self.circuit = None
        self.laps = None
        self.circuit_name = None
        self.championship_circuits = []
        self.championship_circuits_name = {}
        self.current_music = ''
        self.music_volume = 1
        self.sound_volume = 1
        self.fullscreen = False
        self.direction = 'rows'
        self.item = pygame.K_SPACE
        self.pause = pygame.K_p
    
    def set_laps(self, laps):
        self.laps = laps
    
    def get_laps(self):
        return self.laps
        
    def get_mode(self):
        return self.mode
        
    def set_mode(self, mode):
        self.mode = mode
        
    def get_player(self):
        return self.player_selected
        
    def set_player(self, player):
        self.player_selected = player
        
    def get_competitors(self):
        return self.competitors
    
    def set_competitors(self, competitors):
        self.competitors = competitors
    
    def add_competitor(self, competitor):
        self.competitors.append(competitor)
        
    def clear_competitors(self):
        self.competirors = []
    
    def debug(self):
        return self.debug
        
    def level_debug(self):
        return self.debug
    
    def set_circuit(self, circuit):
        self.circuit = circuit

    def set_circuit_name(self, name):
        self.circuit_name = name
    
    def set_championship_circuits(self, circuits):
        self.championship_circuits = circuits
    
    def set_championship_circuit_name(self, circuit_path, name):
        self.championship_circuits_name[circuit_path] = name
    
    def get_championship_circuit_name(self, circuit_path):
        return self.championship_circuits_name[circuit_path]
        
    def add_championship_circuit(self, circuit):
        self.championship_circuits.append(circuit)
    
    def get_championship_circuits(self):
        return self.championship_circuits
    
    def clear_championship_circuits(self):
        self.championship_circuits = []
        
    def get_circuit(self):
        return self.circuit

    def get_circuit_name(self):
        return self.circuit_name
        
    def set_championship(self, cp):
        self.championship = cp
    
    def get_championship(self):
        return self.championship
    
    def get_current_music(self):
        return self.current_music
    
    def set_current_music(self, new_music):
        self.current_music = new_music
    
    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)
   
    def get_music_volume(self):
        return self.music_volume
        
    def set_sound_volume(self, volume):
        self.sound_volume = volume
   
    def get_sound_volume(self):
        return self.sound_volume
    
    def get_fullscreen(self):
        return self.fullscreen
        
    def set_fullscreen(self, fullscreen):
        self.fullscreen = fullscreen
    
    def get_pause_key(self):
        return self.pause 
    
    def get_item_key(self):
        return self.item
    
    def get_direction(self):
        return self.direction
        
    def set_pause_key(self, pause):
        self.pause = pause
    
    def set_item_key(self, item):
        self.item = item
    
    def set_direction(self, direction):
        self.direction = direction
    
