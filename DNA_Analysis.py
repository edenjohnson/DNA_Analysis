# import the requied modules
from tkinter import *
import tkinter as ttk
from tkinter.ttk import Button
import re


# create the window with corresponding labels
root= ttk.Tk()

canvas1 = Canvas(root, width = 700, height = 500, relief = 'raised')
canvas1.pack()

label1 = ttk.Label(root, text='Please enter a sequence and choose a command')
label1.config(font=('helvetica', 15))
canvas1.create_window(350, 25, window=label1)

label2 = ttk.Label(root, text='Enter your sequence:')
label2.config(font=('helvetica', 13))
canvas1.create_window(200, 100, window=label2)

label3 = ttk.Label(root, text='Enter kmer value (as needed):')
label3.config(font=('helvetica', 13))
canvas1.create_window(500, 100, window=label3)

# region for textbox to input DNA sequence
entry1 = Text(root, wrap=WORD, height=10, width=30)
canvas1.create_window(200, 200, window=entry1)

# region for textbox to input k-mer value
entry2 = Entry(root)
canvas1.create_window(475, 128, window=entry2)

# create the DNA class
class DNA:

    def __init__(self, sequence):
        """ Constructor function of the DNA class
            that is an initializer that takes in a sequence
            as a parameter (class attribute). """
        self.sequence = sequence.upper()
        # search the sequence for non-ATCG bases with regex
        if re.search(r'[^ATGC]', self.sequence): 
            Error() 

    def CG_content(self):
        """ Method returns the GC Content of the sequence."""
        sequence_length = len(self.sequence)
        g_count = self.sequence.count('G')
        c_count = self.sequence.count('C')
        gc_content = (g_count + c_count) / sequence_length
        return gc_content

    def kmer_count(self, k):
        """ Method returns the count of kmers. """
        kmers_dict = {}
        # Build the kmer2list dict with "kmer" as key and "list_of_positions"
        ## as value
        for position in range(len(self.sequence) - int(k) + 1):
            # extract the k-mer and assign it to key "kmer"
            kmer = self.sequence[position:position + int(k)]
            # Get the current value of key "kmer" from the dict
            list_of_positions = kmers_dict.get(kmer, [])
            # Add to the list of starting positons the current "position"
            list_of_positions.append(position)
            # Update "list_of_positions" which is the value of key "kmer"
            kmers_dict[kmer] = list_of_positions
        return kmers_dict


    def complementary_DNA(self):
        """ Method transcribes the complementary DNA from the input sequence
            and returns it as a value."""
        trans_dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        # use list comprehension for complementary sequence
        comp_seq = [trans_dict[char] for char in self.sequence\
                    if char in trans_dict]
        return "".join(comp_seq)

    def complementary_RNA(self):
        """ Method transcribes the complementary RNA from the input sequence
            and returns it as a value."""
        trans_dict = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}
        # use list comprehension for complementary sequence
        comp_seq = [trans_dict[char] for char in self.sequence\
                    if char in trans_dict]
        return "".join(comp_seq)

    def translate(self):
        """ Method returns a corresponding amino acid in place of
            a codon to to produce a protein sequence via translation. """
        sequence = self.complementary_RNA()
        amino_acids = {
            'AUA': 'I', 'AUC': 'I', 'AUU': 'I', 'AUG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T',
            'AAC': 'N', 'AAU': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGU': 'S', 'AGA': 'R', 'AGG': 'R',
            'CUA': 'L', 'CUC': 'L', 'CUG': 'L', 'CUU': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P',
            'CAC': 'H', 'CAU': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGU': 'R',
            'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A',
            'GAC': 'D', 'GAU': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G',
            'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S',
            'UUC': 'F', 'UUU': 'F', 'UUA': 'L', 'UUG': 'L',
            'UAC': 'Y', 'UAU': 'Y', 'UAA': '*', 'UAG': '*',
            'UGC': 'C', 'UGU': 'C', 'UGA': '*', 'UGG': 'W'}
        last_codon = len(sequence) - 2
        protein = ""
        for position in range(0, last_codon, 3):
            # translate in all reading frames
            codon = sequence[position:position + 3]
            aa = amino_acids[codon]
            protein += aa
        return protein


# methods to be used in the buttons of the pop-up window by tkinter
def GC_content():
    entry = entry1.get("1.0", 'end-1c')
    sequence = DNA(entry)
    label1 = ttk.Label(root, text=sequence.CG_content())
    canvas1.create_window(300, 330, window=label1)


def Translate():
    entry = entry1.get("1.0", 'end-1c')
    sequence = DNA(entry)
    label1 = ttk.Label(root, text=sequence.translate())
    canvas1.create_window(300, 330, window=label1)


def Get_kmers():
    entry = entry1.get("1.0", 'end-1c')
    k = entry2.get()
    sequence = DNA(entry)
    label1 = ttk.Label(root, text=sequence.kmer_count(k), wraplength=680)
    canvas1.create_window(350, 330, window=label1)


def Complement():
    entry = entry1.get("1.0", 'end-1c')
    sequence = DNA(entry)
    label1 = ttk.Label(root, text=sequence.complementary_DNA(), wraplength=600)
    canvas1.create_window(350, 330, window=label1)

def Error():
    label1 = ttk.Label(root, text = 'Sequence cannot contain non-ATGC bases')
    canvas1.create_window(300, 230, window=label1)


# create the buttons for the dialogue window
button1 = ttk.Button(text='Get Kmers', command=Get_kmers)
canvas1.create_window(100, 440, window=button1)
button2 = ttk.Button(text='Translate', command=Translate)
canvas1.create_window(250, 440, window=button2)
button3 = ttk.Button(text='GC Content', command=GC_content)
canvas1.create_window(400, 440, window=button3)
button4 = ttk.Button(text='Complementary DNA', command=Complement)
canvas1.create_window(570, 440, window=button4)

# execute the window
root.mainloop()
