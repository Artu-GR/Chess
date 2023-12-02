import pygame as py
from pygame.locals import *

class Text:

	def __init__(self, text, pos, **options):
		self.text = text
		self.fontname = None
		self.pos = pos
		self.fontcolor = Color('Green')
		
		# here 50 is the font size
		self.font = py.font.Font(self.fontname, 50)

		# rendering the text in the window
		self.placing = self.font.render(self.text, True,
										self.fontcolor)

		self.rect = self.placing.get_rect()

		# this fix the position of the text
		self.rect.bottomleft = self.pos

	def building(self):

		# put the text on the window
		app.screen.blit(self.placing, self.rect)


class app:

	def __init__(self):

		# Initialize all the parameters to build
		# its base a blank window will appear
		py.init()
		app.screen = py.display.set_mode((540, 340))
		app.t = Text('Text Class in pygame', pos=(100, 150))
		app.running = True

	def run(self):

		# run function
		while app.running:
			for event in py.event.get():
				if event.type == QUIT:
					app.running = False

			app.screen.fill(Color('blue'))

			app.t.building()

			py.display.update()

		py.quit()

# program runs from here
if __name__ == '__main__':

	# calling function from the base class (app)
	app().run()
