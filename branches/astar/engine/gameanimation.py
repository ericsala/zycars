#-*- encoding: utf-8 -*-

import gameobject
import xml.dom.minidom
import data

class GameAnimation(gameobject.GameObject):
    def __init__(self, game_control, path_xml, x, y):
        gameobject.GameObject.__init__(self, game_control)
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        self.parser_basic_info(parse)
        
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        
        self.animations[gameobject.NORMAL].update()
        
        self.image = self.original_sprite[self.animations[gameobject.NORMAL].get_frame()]