#-*- encoding: utf-8 -*-

'''
@file optionmenu.py
Implementa la clase OptionMenu
@author José Jesús Marente Florín
@date Diciembre 2010.
'''

import basicmenu
import data
import resource
import button
import slider
import mainmenu
import xml.dom.minidom
import pygame
import checkbox
import config

class OptionMenu(basicmenu.BasicMenu):
    '''
    @brief Clase que representa el Menú de opciones
    '''
    def __init__(self, game, path_xml):
        '''
        @brief Constructor.
        
        @param game Referencia a game
        @param path_xml Ruta del archivo xml con la configuración
        '''
        basicmenu.BasicMenu.__init__(self, game)
        
        #Cambiamos el título de la ventana
        pygame.display.set_caption("Zycars: Opciones")

        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Obtenemos los elementos básicos del menú
        self.parser_basic_info(parse)
        
        #Declaramos distintos atributos de la clase
        self.text_layers = {}
        self.elements_layers = {}
        self.buttons_layers = {}
        self.images_layers = {}
        self.actual_layer = None
        
        #Recorremos las distintas capas que tendrá el menú
        for element in parse.getElementsByTagName('layer'):
            
            #Obtenemos el nombre de la capa que la indetificará
            name_layer = str(element.getAttribute('name'))
            self.text_layers[name_layer] = []
            self.elements_layers[name_layer] = []
            self.buttons_layers[name_layer] = []
            self.images_layers[name_layer] = {}

            #Fuente que se usará y tamaño de esta
            font_code = str(element.getAttribute('font_code'))
            size = int(element.getAttribute('size'))
            font_temp = resource.get_font(font_code, size)
            
            #Obtenemos los distintos texto que aparecerán por capa
            for text in element.getElementsByTagName('text'):
                
                #Obtenemos texto y posición
                value = text.getAttribute('value')
                posx = int(text.getAttribute('x'))
                posy = int(text.getAttribute('y'))
                
                #Renderizamos
                text_render = font_temp.render(value, True, (0,0,0))
                text_render_rect = text_render.get_rect()
                text_render_rect.x = posx
                text_render_rect.y = posy
                
                #Insertamos en la lista de textos por capa
                self.text_layers[name_layer].append((text_render, 
                                                    text_render_rect))
            
            #Obtenemos los distintos objetos que tendrán cada capa
            #En primer lugar obtenemos los slider
            for slider_option in element.getElementsByTagName('slider'):
                
                #Obtenemos archivo de configuración
                xml_path = str(slider_option.getAttribute('xml_file'))
                
                #Posición
                x = int(slider_option.getAttribute('x'))
                y = int(slider_option.getAttribute('y'))
                
                text = str(slider_option.getAttribute('text'))
                value = 0
                if text == 'sonido':
                    value = int(config.Config().get_sound_volume() * 100)
                else:
                    value = int(config.Config().get_music_volume() * 100)
                #Obtenemos el slider
                new_slider = slider.Slider(xml_path, value, 100, x, y, text)
                
                #Lo introducimos en la lista de sliders
                self.elements_layers[name_layer].append(new_slider)
            
            for check_box in element.getElementsByTagName('checkbox'):
                
                xml_file = str(check_box.getAttribute('xml_file'))
                font_code = str(check_box.getAttribute('font'))
                show_text = False
                text = check_box.getAttribute('text')
                image_code = str(check_box.getAttribute('image_code'))
                image_x = int(check_box.getAttribute('image_x'))
                image_y = int(check_box.getAttribute('image_y'))
                x = int(check_box.getAttribute('x'))
                y = int(check_box.getAttribute('y'))
                
                new_checkbox = checkbox.CheckBox(self, xml_file, text, x, y, 
                                                font_code, image_code, 
                                                image_x, image_y, show_text)
                self.elements_layers[name_layer].append(new_checkbox)
            
            for button_layer in element.getElementsByTagName('button'):
                
                #Ruta del archivo xml con la configuración
                xml_file = str(button_layer.getAttribute('xml_file'))
                
                #Fuente y texto que apareceran en el boton
                font_code = str(button_layer.getAttribute('font'))
                text = button_layer.getAttribute('text')
                
                x = int(button_layer.getAttribute('x'))
                y = int(button_layer.getAttribute('y'))
                show_text = True
                
                #Miramos si se indica si se debe mostrar o no el texto 
                #en el botón
                if button_layer.hasAttribute('show_text'):
                    show_text = button_layer.getAttribute('show_text')
                    show_text = button.strTobool(show_text)
                
                aux_button = button.Button(self, xml_file, text, x, y, 
                                        font_code, show_text)
                    
                #Lo añadimos a la lista de botones
                self.buttons_layers[name_layer].append(aux_button)   
                
            
            for image in element.getElementsByTagName('image_layer'):
                
                image_code = image.getAttribute('image_code')
                x = int(image.getAttribute('x'))
                y = int(image.getAttribute('y'))
                
                self.images_layers[name_layer][image_code] = \
                                        (resource.get_image(image_code), x, y)
            
        for chb in self.elements_layers['Pantalla']:
            if config.Config().get_fullscreen():
                chb.set_checked()
        
        #La capa inicial será la de sonido
        self.actual_layer = "Sonido"
        self.direction = config.Config().get_direction()
        self.pause = 'p' if config.Config().get_pause_key() == \
                                                        pygame.K_p else 'esc'
        self.item = 'space' if config.Config().get_item_key() == \
                                                pygame.K_SPACE else 'enter'
                            
    def update(self):
        '''
        @brief Método encargado de actualizar todos los elementos del menú
        '''
        
        for but in self.buttons_layers[self.actual_layer]:
            but.update()
            #So el cursor está sobre alguno de los botones
            if but.get_selected():
                #Obtenemos su opción
                self.actual_option = but.get_option()
        
        #Actualizamos todos los elementos de la capa actual
        for element in self.elements_layers[self.actual_layer]:
            element.update()
        
        basicmenu.BasicMenu.update(self)
                    
    def draw(self, screen):
        '''
        @brief Método que dibuja todos los elementos del menú en pantalla
        
        @param screen Superficie destino
        '''
        
        #Dibujamos los elementos basicos del juego
        self.draw_basic_elements(screen)
        
        #Dibujamos los texto de la capa actual
        for element in self.text_layers[self.actual_layer]:
            screen.blit(element[0], element[1])

        #Dibujamos los elementos de la capa actual
        for element in self.elements_layers[self.actual_layer]:
            element.draw(screen)
        
        for button_layer in self.buttons_layers[self.actual_layer]:
            button_layer.draw(screen)

        if self.actual_layer == 'Controles':
            screen.blit(self.images_layers[self.actual_layer][self.direction][0],
                    (self.images_layers[self.actual_layer][self.direction][1], 
                    self.images_layers[self.actual_layer][self.direction][2]))
            screen.blit(self.images_layers[self.actual_layer][self.pause][0], 
                    (self.images_layers[self.actual_layer][self.pause][1], 
                    self.images_layers[self.actual_layer][self.pause][2]))
            screen.blit(self.images_layers[self.actual_layer][self.item][0], 
                    (self.images_layers[self.actual_layer][self.item][1], 
                    self.images_layers[self.actual_layer][self.item][2]))
            
        #Dibujamos el cursor
        self.cursor.draw(screen)
        
    def treat_option(self, option):
        '''
        @brief Función encargada de tratar la opción actual del menú seleccionada
        '''
        if option == "Aceptar":
            print "Aceptar"
            self.save_options()
            self.game.change_state(mainmenu.MainMenu(self.game, 
                                                    'menu/mainmenu.xml'))
            
        elif option == "Cancelar":
            print "Cancelar"
            self.game.change_state(mainmenu.MainMenu(self.game, 
                                                    'menu/mainmenu.xml'))

        elif option == "Sonido":
            self.actual_layer = "Sonido"
            
        elif option == "Pantalla":
            self.actual_layer = "Pantalla"
            
        elif option == "Controles":
            self.actual_layer = "Controles"
        
        elif option == "DerechaDireccion":
            print "DerechaDireccion"
            if self.direction == 'letters':
                self.direction = 'rows' 
            else:
                self.direction = 'letters'

        elif option == "DerechaItem":
            print "DerechaItem"
            if self.item == 'space':
                self.item = 'enter' 
            else:
                self.item = 'space'
                
        elif option == "DerechaPausa":
            print "DerechaPausa"
            if self.pause == 'p':
                self.pause = 'esc' 
            else:
                self.pause = 'p'
    
    def save_options(self):
        '''
        @brief Almacena las opciones en la configuración
        '''
        for element in self.elements_layers['Sonido']:
            if element.get_option() == 'sonido':
                config.Config().set_sound_volume(float(element.get_value() / 100.0))
            elif element.get_option() == 'musica':
                config.Config().set_music_volume(float(element.get_value() / 100.0))
            elif element.get_option() == 'silenciar' and element.is_checked():
                config.Config().set_sound_volume(0)
                config.Config().set_music_volume(0)
                
        for element in self.elements_layers['Pantalla']:
            if element.get_option() == 'resolucion':
                if config.Config().get_fullscreen() != element.is_checked():
                    config.Config().set_fullscreen(element.is_checked())
                    self.game.set_screen()
                    
        if self.pause == 'p':
            config.Config().set_pause_key(pygame.K_p)
        else:
            config.Config().set_pause_key(pygame.K_ESCAPE)
        
        if self.item == 'enter':
            config.Config().set_item_key(pygame.K_RETURN)
        else:
            config.Config().set_item_key(pygame.K_SPACE)
        
        config.Config().set_direction(self.direction)


