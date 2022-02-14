""" Pseudocode
1. request input sequence and minimum palindrome length from user
2. compute the reverse complement for the sequence
3. extract all the common sequences from sequence and its reverse complement
4. extract all the palindromes from the common sequences
5. extract and output all the normal palindromes
6. extract and output all the spacer palindromes

sample fasta: https://drive.google.com/file/d/1agEiPPTVbuCPsPQfRVJErASb6TfO3okQ/view?usp=sharing
sample gb: https://drive.google.com/file/d/1ytLxVmzs-uRNwaTWvdVUH42524MAtPH1/view?usp=sharing
"""

import re

def fileInput(): #function to request sequence format choice from user
    fileChoice = int(input("Please choose your input type:\n1 for Raw sequence\n2 for FASTA file\n3 for Genbank file\n"))
    if fileChoice == 1: #choice 1 for raw sequence
        seq = input("\nPlease enter your raw sequence: ")
    
    elif fileChoice == 2: #choice 2 for fasta
        filename = input("\nPlease enter your FASTA filename: ")
        seq = readFASTA(filename) #call readFASTA function

    elif fileChoice == 3: #choice 3 for genbank
        filename = input("\nPlease enter your Genbank filename: ")
        seq = readGB(filename) #call readGB function
    
    else: #fileChoice not in [1,2,3]: #print error message for wrong input
        print("\nInvalid choice. Please try again.","\n")

    seq = seq.upper() #convert sequence to uppercase
    print("\nYour input sequence is:\n",seq,"\n") #print extracted sequence for confirmation
    #request input from user for desired minimum length for palindrome(s)
    minLength = int(input("Please enter the desired minimum length for your palindrome(s): ",))

    return seq,minLength #return sequence which is extracted and converted and the min palindrome length

def readFASTA(filename): #function to extract sequence from FASTA
    fo = open(filename)
    lines = fo.readlines() #read all lines in file
    seq = '' #empty string to store extracted sequence
    
    for line in lines:
        if line.startswith('>'): #ignore the header line which starts with '>'
            pass
        else:
            line = re.sub('\n','',line) #replace newlines with nothing
            seq += line #update seq variable with lines

    return seq #return extracted sequence from fasta
    
def readGB(filename): #function to extract sequence from Genbank
    gb_seq = '^\s+\d+\s+(([a-z_]+\s*)+)' #regular expression (re) pattern to match sequence part    #\s+\d+\s+([a-zA-Z\s]+)+
    fo = open(filename)
    lines = fo.readlines() #read all lines in file
    seq = '' #empty string to store extracted sequence
    
    for line in lines:
        sequenceline = re.search(gb_seq,line) #use re pattern to search for sequence in file
        if sequenceline: #if pattern found
            grp1 = sequenceline.group(1) #for the first subgroup
            sequenceline1 = re.sub('[\s]','',grp1) #replace whitespace with nothing
            seq += sequenceline1 #update seq variable with lines

    return seq #return extracted sequence from genbank

def reverseComplement(seq): #function to commpute reverse complement
    Base = {'A':'T','T':'A','G':'C','C':'G', '_':'_'} #dictionary to store base pair for A,G,C,T and spacer region
    ComplementSeq = "" #empty string to store complement sequence

    for i in range(0, len(seq)): #for every base in the whole original sequence length
        pair = seq[i] #new variable to store each base in original sequence
        ComplementSeq = ComplementSeq + Base[pair] #concatenate the complement base pair together using values from dictionary
    reverseComplementSeq = ComplementSeq[::-1] #reverse the ComplementSeq
    
    return reverseComplementSeq #return the reverse complement sequence

def CommonSequence(seq,revCom,minLength): #function to extract common sequence between the original and reverse complement
    seqLength = len(seq) #compute the sequence length
    commonSequence = [] #empty list to store common sequence

    for i in range(seqLength,minLength-1,-1): #loop from the reverse of sequence
    #until min palindrome length
        for k in range(seqLength-i+1): #loop in the length of short sequence
            if (seq[k:i+k] in revCom): #true if base present in reverse complement
                flag = 1
                for m in range(len(commonSequence)): #loop in the length of list
                    if seq[k:i+k] in commonSequence[m]: #if base is already present in list
                        flag = 0 
                        break #break the loop

                if flag == 1: #if base is not already present in list
                    commonSequence.append(seq[k:i+k]) #add base to the list

    if len(commonSequence): #true if list is not empty
        return(commonSequence) #return list that contains common sequences
    else: #false if list is empty
        pass

def AllPalindrome(allMatches): #function to find all palindromes
    allPalindrome = [] #empty list to store all palindromes
    for sequence in allMatches: #for every sequence in all the common sequence
        #check if that particular sequence is equivalent to its reverse complement (means its a palindrome)
        #and if that sequence does not exist in the list already
        if sequence == reverseComplement(sequence) and sequence not in allPalindrome: #true
            allPalindrome.append(sequence) #add that sequence to the list

    return allPalindrome #return all the palindromes in the whole sequence

def NormalPalindrome(allPalindrome): #function to find normal palindromes (without spacer region)
    normalPalindrome = [] #empty list to store normal palindromes
    for sequence in allPalindrome: #for every sequence in all the palindromes
        if '_' not in sequence: #filter out palindromes that doesnt contain '_'
            normalPalindrome.append(sequence) #add that palindrome to the list

    if len(normalPalindrome): #print out all the normal palindromes if available
        normalPalindrome = ', '.join(normalPalindrome) #convert normal palindrome list to string for output
        print("\nNormal palindromes (non-repeating): \n",normalPalindrome,"\n") 
    else:
         print("There are no normal palindromes that can be detected.\n")

def SpacerPalindrome(allPalindrome): #function to find spacer palindromes
    allPalindrome = ' '.join(allPalindrome) #convert list of all palindromes to string for re
    spacerPalindrome = re.findall(r'[AGCT]+_+[AGCT]+',allPalindrome) #find all spacer palindromes using re

    if len(spacerPalindrome): #print out all the spacer palindromes if available
        spacerPalindrome = ', '.join(spacerPalindrome) #convert spacer palindrome list to string for output
        print("Reverse-complement non-repeating palindromes with an intervening spacer region: \n",spacerPalindrome,"\n")
    else:
        print("There is no reverse-complement non-repeating palindromes with an intervening spacer region that can be detected.\n")

seq,minLength = fileInput() #call function fileInput()
revCom = reverseComplement(seq) #call function reverseComplement()
allMatches = CommonSequence(seq,revCom,minLength) #call function CommonSequence()
allPalindrome = AllPalindrome(allMatches) #call function AllPalindrome()
NormalPalindrome(allPalindrome) #call function NormalPalindrome()
SpacerPalindrome(allPalindrome) #call function SpacerPalindrome()