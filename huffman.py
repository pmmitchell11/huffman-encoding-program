def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""

    afreq = a.freq
    bfreq = b.freq

    achar = a.char
    bchar = b.char

    if afreq < bfreq:  # if a's freq is less than b's freq
        return True
    if afreq == bfreq:  # if a and b have same freq count
        return achar < bchar  # return true if ascii value of a is less than b's, false otherwise

    return False


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the frequency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __lt__(self, other):
        return comes_before(self, other)


def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""

    afreq = a.freq
    bfreq = b.freq
    freq_sum = afreq + bfreq

    if a.char <= b.char:  # if ascii value of a is <= b's ascii
        huffnode = HuffmanNode(a.char, freq_sum)  # new huffman node will take lower ascii value for char
    else:
        huffnode = HuffmanNode(b.char, freq_sum)

    huffnode.left = a
    huffnode.right = b

    return huffnode


def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file"""

    try:
        f = open(filename, 'r')  # open a file and read it
    except:
        raise FileNotFoundError

    frequency = [0]*256  # creates a array of size 256 (0-255)

    for line in f:  # go through each line in the text file
        for c in line:  # go through each character in the line
            ascii_val = ord(c)  # get ascii value
            frequency[ascii_val] += 1  # in the freq array, increment the index value (== ascii) value b/c it was seen

    f.close()

    return frequency


def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""

    zero_counter = 0
    for item in char_freq:
        if item == 0:
            zero_counter += 1

    if zero_counter == 256:
        return None


    huffnode_list = []  # list of huffman nodes of non-zero frequency

    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            huffnode = HuffmanNode(i, char_freq[i])
            huffnode_list.append(huffnode)

    huffnode_list.sort(reverse=True)  # sorted list of huffman nodes by frequency count


    while len(huffnode_list) > 1:
        combined_node = combine(huffnode_list.pop(), huffnode_list.pop())

        huffnode_list.append(combined_node)

        huffnode_list.sort(reverse=True)

    return huffnode_list[0]


def find_leaves(root, code, array):
    ''' Finds all possible root-to-leaf paths and adds a '1' to the code if you go right,
        adds a '0' to the code if you go left '''
    if root is None:
        return array
    if root.right is None and root.left is None:
        char = root.char
        array[char] = code
        return array
    else:
        find_leaves(root.left, code + '0', array)
        find_leaves(root.right, code + '1', array)
        return array



def create_code(root_node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location"""

    array = [''] * 256

    return find_leaves(root_node, '', array)

def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list associated with "aaabbbbcc, would return “97 3 98 4 99 2” """

    header = []

    for i in range(len(freqs)):
        if freqs[i] == 0:
            pass
        else:
            header.append(str(i))
            header.append(str(freqs[i]))

    return ' '.join(header)


def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take note of special cases - empty file and file with only one unique character"""

    try:
        f = open(in_file, 'r')  # open a file and read it
    except:
        raise FileNotFoundError

    out = open(out_file, 'w', newline='')


    char_freq = cnt_freq(in_file)

    hufftree = create_huff_tree(char_freq)

    header = create_header(char_freq)

    if hufftree is None:
        out.write('')
    elif hufftree.right is None and hufftree.left is None:  # then code is '', just put header
        out.write(header)
    else:
        code = create_code(hufftree)

        out.write(header)
        out.write('\n')

        for line in f:
            for char in line:
                ascii = ord(char)
                out.write(code[ascii])

    out.close()
    f.close()


def parse_header(header):
    ''' Function to create frequency list from the header of the encoded input file '''

    res = [i for i in header.split()]  # makes split list

    frequency_list = [0] * 256

    # makes the freq list based on the header info
    for i in range(0, len(res), 2):
        ascii = int(res[i])
        cnt = int(res[i+1])

        frequency_list[ascii] = cnt

    return frequency_list


def huffman_decode(encoded_file, decode_file):
    try:
        f = open(encoded_file, 'r')  # open a file and read it
    except:
        raise FileNotFoundError

    out = open(decode_file, 'w', newline='')

    header = f.read().split('\n')[0]

    f.seek(0)
    num_in_header = f.read().split(' ')

    if header == '':
        out.write('')
        f.close()
        out.close()
        return out
    elif len(num_in_header) == 2:
        char = chr(int(num_in_header[0]))
        res = int(num_in_header[1]) * char
        out.write(res)
        f.close()
        out.close()
        return out


    freq_list = parse_header(header)

    hufftree = create_huff_tree(freq_list)

    # gets second line from input file (which is the coded/compressed file)
    f.seek(0)

    code = f.read().split('\n')[1]

    root = hufftree

    decoded = decoder_helper(hufftree, root, code)

    out.write(decoded)

    f.close()
    out.close()

    return out


def decoder_helper(hufftree, root, code):
    decoded = []

    for c in code:
        if root.right is None and root.left is None:
            decoded.append(chr(root.char))
            root = hufftree
            if c == '1':
                root = root.right
            elif c == '0':
                root = root.left
        elif c == '1':  # move right
            root = root.right
        elif c == '0':  # move left
            root = root.left

    decoded.append(chr(root.char))
    res = ''.join(decoded)

    return res