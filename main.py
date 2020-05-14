import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.data import load

import re

from tkinter import *
from tkinter import filedialog as fd

import docx

lemmatizer = WordNetLemmatizer()
tag_dict = {
            "JJ": wn.ADJ,
            "JJR": wn.ADJ,
            "JJS": wn.ADJ,
            "NN": wn.NOUN,
            "NNP": wn.NOUN,
            "NNS": wn.NOUN,
            "NNPS": wn.NOUN,
            "VB": wn.VERB,
            "VBN": wn.VERB,
            "VBG": wn.VERB,
            "VBZ": wn.VERB,
            "VBP": wn.VERB,
            "VBD": wn.VERB,
            "RB": wn.ADV,
            "RBR": wn.ADV,
            "RBS": wn.ADV,
            }

def pos_tag_sentence(sent):
    postgs = nltk.pos_tag(nltk.word_tokenize(sent))
    rtgs = list()
    i = 0
    pos = 1
    while i < len(postgs):
        pt = postgs[i]
        if re.search(r"[A-Za-z]+", pt[0]) != None:
            lemma = str()
            if pt[1] in tag_dict:
                lemma = lemmatizer.lemmatize(pt[0], pos=tag_dict.get(pt[1]))
            else:
                lemma = lemmatizer.lemmatize(pt[0])
            rtgs.append((lemma.upper(), pt[1]))
            pos += 1
        i += 1
    return rtgs

tagdict = load('help/tagsets/upenn_tagset.pickle')

filename = str()

def get_text():
    global filename
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def get_filename():
    global filename
    filename = fd.askopenfilename(filetypes=(("DOCX files", "*.docx"),))

root = Tk()

grammar = r"""
        P: {<IN>}
        V: {<V.*|MD>}
        N: {<NN.*>}
        JJP: {<RB|RBR|RBS|JJ|JJR|JJS|CD>}
        NP: {<N|PP>+<DT|PR.*|JJP|CC>}
        NP: {<PDT>?<DT|PR.*|JJP|CC><N|PP>+}
        PP: {<P><N|NP>}
        VP: {<NP|N|PR.*><V|VP>+}
        VP: {<V><NP|N>}
        VP: {<V><JJP>}
        VP: {<VP><PP>}
        """

def build_syntax_tree():
    txt = get_text()
    sentences = nltk.sent_tokenize(txt)
    for sent in sentences:
        tsent = pos_tag_sentence(sent)
        ch = nltk.RegexpParser(grammar)
        tree = ch.parse(tsent)
        tree.draw()

def help_window():
    children = Toplevel(root)
    children.title('Help')

    helpmsg = """
1. Open a file
2. Press "Build syntax tree" button
3. See syntax tree

S -- Start element(whole sentece)
P -- Preposition
N -- Noun
V -- Verbs and modals
JJP -- Adjective part(Adjectives, adverbs and cordinals)
NP -- Noun part
PP -- Prepositional part
VP -- Verbal part
    """

    text = Text(children, height=20, width=100)
    scroll = Scrollbar(children)
    scroll.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    text.insert(END, helpmsg)

root.title("Syntax tree builder")
root.geometry("500x300")

help = Button(text="Open file", command=get_filename)
help.place(relx=.5, rely=.1, anchor="c")

help = Button(text="Build syntax tree", command=build_syntax_tree)
help.place(relx=.5, rely=.5, anchor="c")

help = Button(text="Help", command=help_window)
help.place(relx=.5, rely=.9, anchor="c")

root.mainloop()
