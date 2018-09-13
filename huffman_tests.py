import unittest
import filecmp
from huffman import *

class TestList(unittest.TestCase):
   def test_cnt_freq(self):
      freqlist	= cnt_freq("file2.txt")
      anslist = [2, 4, 8, 16, 0, 2, 0] 
      self.assertListEqual(freqlist[97:104], anslist)

   def test_create_huff_tree(self):
      freqlist = cnt_freq("file2.txt")
      hufftree = create_huff_tree(freqlist)
      self.assertEqual(hufftree.freq, 32)
      self.assertEqual(hufftree.char, 97)
      left = hufftree.left
      self.assertEqual(left.freq, 16)
      self.assertEqual(left.char, 97)
      right = hufftree.right
      self.assertEqual(right.freq, 16)
      self.assertEqual(right.char, 100)

   def test_create_header(self):
      freqlist = cnt_freq("file2.txt")
      self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

   def test_create_code(self):
      freqlist = cnt_freq("file2.txt")
      hufftree = create_huff_tree(freqlist)
      codes = create_code(hufftree)
      self.assertEqual(codes[ord('d')], '1')
      self.assertEqual(codes[ord('a')], '0000')
      self.assertEqual(codes[ord('f')], '0001')

   def test_01_textfile(self):
      huffman_encode("file1.txt", "file1_out.txt")
      # capture errors by running 'filecmp' on your encoded file with a *known* solution file
      self.assertTrue(filecmp.cmp("file1_out.txt", "file1_soln.txt"))

   def test_02_textfile(self):
      huffman_encode("file2.txt", "file2_out.txt")
      # capture errors by running 'filecmp' on your encoded file with a *known* solution file
      self.assertTrue(filecmp.cmp("file2_out.txt", "file2_soln.txt"))

   def test_03_textfile(self):
      huffman_encode("multiline.txt", "multiline_out.txt")
      # capture errors by running 'filecmp' on your encoded file with a *known* solution file
      self.assertTrue(filecmp.cmp("multiline_out.txt", "multiline_soln.txt"))

   def test_04_textfile(self):
      huffman_encode("empty.txt", "empty_out.txt")
      # capture errors by running 'filecmp' on your encoded file with a *known* solution file
      self.assertTrue(filecmp.cmp("empty.txt", "empty_out.txt"))

   def test_05_textfile(self):
      huffman_encode("single.txt", "single_out.txt")
      # capture errors by running 'filecmp' on your encoded file with a *known* solution file
      self.assertTrue(filecmp.cmp("single_out.txt", "single_soln.txt"))

   def test_06_textfile(self):
      huffman_encode("declaration.txt", "declaration_out.txt")
      # capture errors by running 'filecmp' on your encoded file with a *known* solution file
      self.assertTrue(filecmp.cmp("declaration_out.txt", "declaration_soln.txt"))
      huffman_decode("declaration_out.txt", "declaration_decode.txt")
      self.assertTrue(filecmp.cmp("declaration.txt", "declaration_decode.txt"))

   def test_07_textfile(self):
      huffman_decode("multiline_soln.txt", "xd.txt")
      self.assertTrue(filecmp.cmp("multiline.txt", "xd.txt"))

   def test_08_textfile(self):
      huffman_decode("empty.txt", "xd_empty.txt")
      self.assertTrue(filecmp.cmp("xd_empty.txt", "empty.txt"))

   def test_09_textfile(self):
      huffman_decode("single_out.txt", "xd_single.txt")
      self.assertTrue(filecmp.cmp("single.txt", "xd_single.txt"))



   def test_comes_before1(self):
      node1 = HuffmanNode('a', 10)
      node2 = HuffmanNode('b', 11)

      self.assertTrue(comes_before(node1, node2))
      self.assertFalse(comes_before(node2, node1))

   def test_set_left1(self):
      node1 = HuffmanNode('a', 10)
      node2 = HuffmanNode('b', 10)
      node3 = HuffmanNode('c', 10)

      node1.set_left(node2)
      node1.set_right(node3)

      self.assertEqual(node1.right, node3)
      self.assertEqual(node1.left, node2)

   def test_find_leaves1(self):
      root = None
      array = [] * 256
      self.assertEqual(find_leaves(root, '', array), array)

   def test_empty(self):
      freq = cnt_freq("empty.txt")
      hufftree = create_huff_tree(freq)
      self.assertEqual(hufftree, None)


   def test_exceptions(self):
      with self.assertRaises(FileNotFoundError):
         cnt_freq('memes.txt')
      with self.assertRaises(FileNotFoundError):
         huffman_encode('memes.txt', 'xd')
      with self.assertRaises(FileNotFoundError):
         huffman_decode('memes.txt', 'xd')





if __name__ == '__main__': 
   unittest.main()
