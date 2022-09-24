#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math


#Global functions
def clean_text(txt):
    """returns a list containing the words in txt after it has been “cleaned”"""
    txt = txt.lower()
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')
    txt = txt.replace(';', '')
    txt = txt.replace(':', '')
    txt = txt.replace('"', '')
    return txt.split()
    
def stem(s):
    """ accepts a string as a parameter and returns the stem of s"""
    length = len(s)
    
    if length >= 2:
        if s[-1] == 's':
            s = s[:-1]
    
        if s[-1] == 'y':
            s = s[:-1] + 'i'
        
    if length >= 4:
        if s[-2:] == 'er':
            if s[-3] == s[-4]:
                s = s[:-3]
            else:
                s = s[:-2]
        
        if s[-2:] == 'ly':
            s = s[:-2]
        
    if length >= 8:
        if s[-3:] == 'ing':
            if s[-4] == s[-5]:
                s = s[:-4]
            else:
                s = s[:-3]
                
        if s[-3:] == 'est':
            if s[-4] == s[-5]:
                s = s[:-4]
            else:
                s = s[:-3]
            
        if s[-4:] == 'less':
            s = s[:-4]
            
        if s[-4:] == 'ness':
            s = s[:-4]
            
        if s[-4:] == 'ment':
            s = s[:-4]
            
        if s[-3:] == 'ful':
            s = s[:-3]
            
    else:
        return s

    return s

def compare_dictionaries(d1, d2):
    """takes two feature dictionaries d1 and d2 as inputs, and computes and returns their log similarity score"""
    score = 0
    total = sum(d1.values())
    
    for i in d2:
        if i in d1:
            s = math.log(d1[i]/total)
            score += d2[i] * s
        else:
            s = math.log(0.5/total)
            score += d2[i] * s
            
    return score

#Class and Methods
class TextModel:
    """ a class that stores methods for a body of text"""
    
    def __init__(self, model_name):
        """constructs a new TextModel object by accepting a string model_name as a parameter and initializing name, words, and, word_lengths"""
        
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
        
    def __repr__(self):
        """returns a string that includes the name of the model as well as the sizes of the dictionaries for each feature of the text"""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: '+ str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuations: ' + str(len(self.punctuation))
        return s
    
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
       to all of the dictionaries in this text model.
       """
        
        ss = s.replace('! ', '. ')
        ss = s.replace('? ', '. ')
        sentence_list = ss.split('. ')
        
        for sentence in sentence_list:
            words = clean_text(sentence)
            length = len(words)
            if length not in self.sentence_lengths:
                self.sentence_lengths[length] = 1
            else:
                self.sentence_lengths[length] += 1
        
    # Add code to clean the text and split it into a list of words.
        word_list = clean_text(s)

    # Template for updating the words dictionary.
        for w in range(len(word_list)):
            if word_list[w] not in self.words:
                self.words[word_list[w]] = 1
            else:
                self.words[word_list[w]] += 1

    # Add code to update other feature dictionaries.
        for w in word_list:
            word_length = len(w)
            if word_length not in self.word_lengths:
                self.word_lengths[word_length] = 1
            else:
                self.word_lengths[word_length] += 1
    
        for w in range(len(word_list)):
            st = stem(word_list[w])
            if st not in self.stems:
                self.stems[st] = 1
            else:
                self.stems[st] += 1
                
        for c in s:
            if c in '.!?,")(][-_*':
                if c not in self.punctuation:
                    self.punctuation[c] = 1
                else:
                    self.punctuation[c] += 1
            else:
                continue
        
    
    
    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model"""
        file = open(filename, 'r', encoding='utf8', errors='ignore')
        text =file.read()
        self.add_string(text)
        
    def save_model(self):
        """saves the TextModel object self by writing its various feature dictionaries to files"""
        f1 = open(self.name + '_' + 'words', 'w')
        f1.write(str(self.words))
        f1.close()
        
        f2 = open(self.name + '_' + 'word_lengths', 'w')
        f2.write(str(self.word_lengths))
        f2.close()
        
        f3 = open(self.name + '_' + 'stems', 'w')
        f3.write(str(self.stems))
        f3.close()
        
        f4 = open(self.name + '_' + 'sentence_lengths', 'w')
        f4.write(str(self.sentence_lengths))
        f4.close()
        
        f5 = open(self.name + '_' + 'punctuation', 'w')
        f5.write(str(self.punctuation))
        f5.close()
        
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object from their files and assigns them to the attributes of the called TextModel."""
        f1 = open(self.name + '_' + 'words', 'r')
        d_str1 = f1.read()
        f1.close()
        self.words = dict(eval(d_str1))
        
        f2 = open(self.name + '_' + 'word_lengths', 'r')
        d_str2 = f2.read()
        f2.close()
        self.word_lengths = dict(eval(d_str2))
        
        f3 = open(self.name + '_' + 'stems', 'r')
        d_str3 = f3.read()
        f3.close()
        self.stems = dict(eval(d_str3))
        
        f4 = open(self.name + '_' + 'sentence_lengths', 'r')
        d_str4 = f4.read()
        f4.close()
        self.sentence_lengths = dict(eval(d_str4))
        
        f5 = open(self.name + '_' + 'punctuation', 'r')
        d_str5 = f5.read()
        f5.close()
        self.punctuation = dict(eval(d_str5))
        
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring the similarity of self and other – one score for each type of feature (words, word lengths, stems, sentence lengths, and your additional feature)"""
    
        words = compare_dictionaries(other.words, self.words)
        word_lengths = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems = compare_dictionaries(other.stems, self.stems)
        sentence_lengths = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation = compare_dictionaries(other.punctuation, self.punctuation)
        
        scores_list = [words, word_lengths, stems, sentence_lengths, punctuation]
    
        return scores_list
    
    def classify(self, source1, source2):
        """compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2) and determines which of these other TextModels is the more likely source of the called TextModel"""
        
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
            
        print(scores1)
        print(scores2)
        
        weighted_sum1 = 10*scores1[0] + 6*scores1[1] + 7*scores1[2] + 5*scores1[3] + 4*scores1[4]
        weighted_sum2 = 10*scores2[0] + 6*scores2[1] + 7*scores2[2] + 5*scores2[3] + 4*scores2[4]
        
        if weighted_sum1 > weighted_sum2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)
    
def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)  
    
def run_tests():
    """ """
    source1 = TextModel('The Beatles')
    source1.add_file('beatles.txt')

    source2 = TextModel('Katy Perry')
    source2.add_file('perry.txt')

    new1 = TextModel('In My Life - The Beatles')
    new1.add_file('inmylife.txt')
    new1.classify(source1, source2)

    new2 = TextModel('Teenage Dream - Katy Perry')
    new2.add_file('teenagedream.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('Sorry - Justin Bieber')
    new3.add_file('sorry.txt')
    new3.classify(source1, source2)
        
    new4 = TextModel('The Raven - Edgar Allan Poe')
    new4.add_file('theraven.txt')
    new4.classify(source1, source2)
        
