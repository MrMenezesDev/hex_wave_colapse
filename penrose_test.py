import unittest
from hex_wave_collapse import Cell, Tile

class PenroseTestCell(unittest.TestCase):

	def setUp(self):
		# Configuração inicial para os testes
		self.tile1 = Tile(edges=[0, 0, 1, 1, 0, 0], image=None) # 0,0
		self.tile2 = Tile(edges=[1, 1, 0, 0, 0, 0], image=None) # 0,1
		self.tile3 = Tile(edges=[0, 0, 0, 0, 1, 1], image=None) # 1,0
		self.tile4 = Tile(edges=[0, 0, 0, 0, 0, 0], image=None) # 1,1
		
		options=[self.tile1, self.tile2, self.tile3, self.tile4]
  
		self.cell00 = Cell(col=0, row=0, options=options)
		self.cell01 = Cell(col=0, row=1, options=options)
		self.cell10 = Cell(col=1, row=0, options=options)
		self.cell11 = Cell(col=1, row=1, options=options)
		self.cell21 = Cell(col=2, row=1, options=options)
		self.cell22 = Cell(col=2, row=2, options=options)
		self.cell12 = Cell(col=1, row=2, options=options)
		self.cell02 = Cell(col=0, row=2, options=options)
		self.cell20 = Cell(col=2, row=0, options=options)

	# Teste 1,0
	def test_update_options_vertical_01(self):
		self.cell10.tile = self.tile1
		self.cell11.update_options(self.cell10)
		self.assertEqual(self.cell11.options, [self.tile2])
	
 	# Teste 1,2
	def test_update_options_vertical_02(self):
		self.cell12.tile = self.tile4
		self.cell11.update_options(self.cell12)
		self.assertEqual(self.cell11.options, [self.tile2, self.tile3, self.tile4])

 	# Teste 2,2
	def test_update_options_diagonal_02(self):
		self.cell22.tile = self.tile3
		self.cell11.update_options(self.cell22)
		self.assertEqual(self.cell11.options, [self.tile1])
 	
    # Teste 0,2
	def test_update_options_diagonal_04(self):
		self.cell02.tile = self.tile2
		self.cell11.update_options(self.cell02)
		self.assertEqual(self.cell11.options, [self.tile3])

	# # Teste 2,1
	# def test_update_options_diagonal_01(self):
	# 	self.cell21.tile = self.tile3
	# 	self.cell11.update_options(self.cell21)
	# 	self.assertEqual(self.cell11.options, [self.tile2])

if __name__ == '__main__':
	unittest.main()