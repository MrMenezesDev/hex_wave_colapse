import unittest
from hex_wave_collapse import Cell, Tile

class UpdateOpTestCell(unittest.TestCase):

	def setUp(self):
		# Configuração inicial para os testes
		self.tile0 = Tile(edges=[1, 0, 0, 0, 0, 0], image=None)
		self.tile1 = Tile(edges=[0, 1, 0, 0, 0, 0], image=None)
		self.tile2 = Tile(edges=[0, 0, 1, 0, 0, 0], image=None)
		self.tile3 = Tile(edges=[0, 0, 0, 1, 0, 0], image=None)
		self.tile4 = Tile(edges=[0, 0, 0, 0, 1, 0], image=None)
		self.tile5 = Tile(edges=[0, 0, 0, 0, 0, 1], image=None)

		self.options=[self.tile0, self.tile1, self.tile2, self.tile3, self.tile4, self.tile5]
  
		self.cell01 = Cell(col=0, row=1, options=self.options)
		self.cell10 = Cell(col=1, row=0, options=self.options)
		self.cell11 = Cell(col=1, row=1, options=self.options)
		self.cell21 = Cell(col=2, row=1, options=self.options)
		self.cell22 = Cell(col=2, row=2, options=self.options)
		self.cell12 = Cell(col=1, row=2, options=self.options)
		self.cell02 = Cell(col=0, row=2, options=self.options)

	def test_update_options_vertical_101(self):
		self.cell10.tile = self.tile3
		self.cell11.update_options(self.cell10)
		self.assertEqual(self.cell11.options, [self.tile0])
	
	def test_update_options_vertical_100(self):
		self.cell10.tile = self.tile0
		self.cell11.update_options(self.cell10)
		self.assertEqual(self.cell11.options, [self.tile1, self.tile2, self.tile3, self.tile4, self.tile5])

	def test_update_options_diagonal_210(self):
		self.cell21.tile = self.tile0
		self.cell11.update_options(self.cell21)
		self.assertEqual(self.cell11.options, [self.tile0, self.tile2, self.tile3, self.tile4, self.tile5])

	def test_update_options_diagonal_211(self):
		self.cell21.tile = self.tile4
		self.cell11.update_options(self.cell21)
		self.assertEqual(self.cell11.options, [self.tile1])

	def test_update_options_diagonal_220(self):
		self.cell22.tile = self.tile0
		self.cell11.update_options(self.cell22)
		self.assertEqual(self.cell11.options, [self.tile0, self.tile1, self.tile3, self.tile4, self.tile5])

	def test_update_options_diagonal_221(self):
		self.cell22.tile = self.tile5
		self.cell11.update_options(self.cell22)
		self.assertEqual(self.cell11.options, [self.tile2])

	def test_update_options_vertical_121(self):
		self.cell12.tile = self.tile0
		self.cell11.update_options(self.cell12)
		self.assertEqual(self.cell11.options, [self.tile3])
	
	def test_update_options_vertical_120(self):
		self.cell12.tile = self.tile3
		self.cell11.update_options(self.cell12)
		self.assertEqual(self.cell11.options, [self.tile0, self.tile1, self.tile2, self.tile4, self.tile5])

	def test_update_options_diagonal_020(self):
		self.cell02.tile = self.tile0
		self.cell11.update_options(self.cell02)
		self.assertEqual(self.cell11.options, [self.tile0, self.tile1, self.tile2, self.tile3, self.tile5])

	def test_update_options_diagonal_021(self):
		self.cell02.tile = self.tile1
		self.cell11.update_options(self.cell02)
		self.assertEqual(self.cell11.options, [self.tile4])

	def test_update_options_diagonal_010(self):
		self.cell01.tile = self.tile0
		self.cell11.update_options(self.cell01)
		self.assertEqual(self.cell11.options, [self.tile0, self.tile1, self.tile2, self.tile3, self.tile4])

	def test_update_options_diagonal_011(self):
		self.cell01.tile = self.tile2
		self.cell11.update_options(self.cell01)
		self.assertEqual(self.cell11.options, [self.tile5])

if __name__ == '__main__':
	unittest.main()