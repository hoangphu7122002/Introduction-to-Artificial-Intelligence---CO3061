import pygame, sys
import tents.gen_board as tents_gen_board
import tents.search as tents_search

import battleships.gen_board as battleships_gen_board
import battleships.blind_search as battleships_blind_search
import battleships.geneticAI as battleships_geneticAI_search

red = (255,69,0)
green = (0, 255, 130)
black = (0, 0, 0)
white = (255,255,255)

class Button:
	def __init__(self,text,width,height,pos,elevation,gui_font,screen):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
		self.screen = screen

	def draw(self):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(self.screen,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(self.screen,self.top_color, self.top_rect,border_radius = 12)
		self.screen.blit(self.text_surf, self.text_rect)
		# self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					return True
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'
		return False

class GUI_MENU(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500,480))
        pygame.display.set_caption('Gui Menu')
        self.clock = pygame.time.Clock()
        self.gui_font = pygame.font.Font('tents\\FileGame\\04B_19.TTF',30)
        self.bg_tents = pygame.image.load("images\\tents_v2.png")
        self.bg_battleship = pygame.image.load("images\\bs_v2.gif")
        self.main_bg = pygame.image.load("images\\tent_bg2.jpg")
    
    def render_font(self,text,color,x,y):
        surface = self.gui_font.render(text,True,color)
        rect = surface.get_rect(center = (x,y))
        self.screen.blit(surface,rect)
    
    def main_menu(self):
        button_tent = Button('TENTS',200,50,(150,265),5,self.gui_font,self.screen)
        button_battle_ship = Button('BATTLE SHIP',200,50,(150,340),5,self.gui_font,self.screen)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('#DCDDD8')
            self.screen.blit(self.main_bg,(0,0))
            self.render_font('MAIN MENU',white,250,100)
            button_tent.draw()
            button_battle_ship.draw()
            
            if button_tent.check_click():
                self.tent()
                return None
            if button_battle_ship.check_click():
                self.battle_ship()
                return None
            pygame.display.update()
            self.clock.tick(60)
            
    def battle_ship(self):  
        button_genetic_AI = Button('GENETIC AI',200,50,(150,265),5,self.gui_font,self.screen)
        button_DFS = Button('DFS',200,50,(150,340),5,self.gui_font,self.screen)
        undo = Button('UNDO',200,50,(150,415),5,self.gui_font,self.screen)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('#DCDDD8')
            self.screen.blit(self.bg_battleship,(0,0))
            self.render_font('BATTLE SHIP',white,250,100)
            button_DFS.draw()
            button_genetic_AI.draw()
            undo.draw()
            
            if undo.check_click():
                self.main_menu()
                return None
            
            if button_DFS.check_click():
                self.screen_level('DFS BATTLE_SHIPS')
                return None
            if button_genetic_AI.check_click():
                self.screen_level('GENETIC_AI BATTLE_SHIPS')
                return None
            pygame.display.update()
            self.clock.tick(60)
        
    def tent(self):  
        A_star_button = Button('A STAR',200,50,(150,265),5,self.gui_font,self.screen)
        DFS_button = Button('DFS',200,50,(150,340),5,self.gui_font,self.screen)
        undo = Button('UNDO',200,50,(150,415),5,self.gui_font,self.screen)
        
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('#DCDDD8')
            self.screen.blit(self.bg_tents,(0,0))
            self.render_font('TENT',white,250,100)
            A_star_button.draw()
            DFS_button.draw()
            undo.draw() 
            
            if undo.check_click():
                self.main_menu()
            if A_star_button.check_click():
                self.screen_level('A* TENTS')
                return None
            if DFS_button.check_click():
                self.screen_level('DFS TENTS')
                return None
            pygame.display.update()
            self.clock.tick(60)
        
    def screen_level(self,text):
        level = []
        level.append(Button('6x6',200,50,(40,265),5,self.gui_font,self.screen))
        level.append(Button('8x8',200,50,(40,340),5,self.gui_font,self.screen))
        level.append(Button('10x10',200,50,(260,265),5,self.gui_font,self.screen))
        level.append(Button('15x15',200,50,(260,340),5,self.gui_font,self.screen))
        
        dict_level = {x : y for x,y in zip([0,1,2,3],[6,8,10,15])}
        
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('#DCDDD8')
            bg_name = text.split(' ')
            if bg_name[1] == 'TENTS':
                self.screen.blit(self.bg_tents,(0,0))
            else:
                self.screen.blit(self.bg_battleship,(0,0))
            self.render_font(text,white,250,100)
            
            for lev in level:
                lev.draw()
            
            for i,lev in enumerate(level):
                if lev.check_click():
                    if bg_name[1] == 'TENTS':
                        gb = tents_gen_board.Board(dict_level[i])
                        board = gb.get_board()
                        row_constraint = gb.get_row_constraint()
                        col_constraint = gb.get_col_constraint()
                        tree_pos = gb.get_tree_pos()
    
                        agent = tents_search.Search(board,row_constraint,col_constraint,tree_pos)
                        if bg_name[0] == "DFS": 
                            agent.DFS()
                        else:
                            agent.A_star()
                    else:
                        gen_object = battleships_gen_board.gen_board(dict_level[i])
                        board = gen_object.get_board()
                        row_constraint = gen_object.get_row_constraint()
                        col_constraint = gen_object.get_col_constraint()
                        
                        if bg_name[0] == "DFS": 
                            gen = battleships_blind_search.DFS(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint(), len(gen_object.get_board()))
                            gen.solve()
                            gen.show()
                        else:
                            gen = battleships_geneticAI_search.Genetic(gen_object.get_board(), gen_object.get_ship(), gen_object.get_row_constraint(), gen_object.get_col_constraint(), len(gen_object.get_board()))
                            gen.solve()
                            gen.show()
                    return None
                    
            
            pygame.display.update()
            self.clock.tick(60)

a = GUI_MENU()
a.main_menu()