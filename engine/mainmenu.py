#-*- encoding: utf-8 -*-

import state
import data
import resource
import button
import keyboard
import pygame
import cursor
import basicmenu
import xml.dom.minidom
import unicodedata

class MainMenu(basicmenu.BasicMenu):
    def __init__(self, game, path_xml):
        basicmenu.BasicMenu.__init__(self, game)
        
        pygame.display.set_caption("Zycars: Menú Principal")
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        self.parser_basic_info(parse)

    def draw(self, screen):
        
        self.draw_basic_elements(screen)
        
        for button in self.buttons:
            button.draw(screen)
        
        self.cursor.draw(screen)
    
    def update(self):
        
        self.actual_option = None
        for button in self.buttons:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        if self.actual_option:
            self.cursor.over()
        else:
            self.cursor.normal()
        
        self.cursor.update()

        if pygame.mouse.get_pressed()[0]:
            self.treat_option()
            
    def treat_option(self):
        
        if self.actual_option == u"Carrera Rápida":
            print "Elegido: Carrera Rapida"
        elif self.actual_option == "Campeonato":
            print "Elegido: Campeonato"
        elif self.actual_option == "Contrarreloj":
            print "Ha elegido: Contrarreloj"
        elif self.actual_option == "Opciones":
            print "Ha elegido: Opciones"
        elif self.actual_option == "Salir":
            print "Ha elegido: Salir"
            keyboard.set_quit(True)
