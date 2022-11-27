#Program Name: Term-Document Co-Occurrence
#Author: Victor Paul LaBrie
#Date: November 27th, 2022
#Problem: Write a program in the language of your 
# choice that creates a term by document co-occurrence 
# matrix for a collection of books, and then measures 
# the pairwise cosine similarity between every pair of 
# these books.
import sys
import re
#Get arguments
lower = sys.argv[1]
upper = sys.argv[1]
textFiles = sys.argv[3:]
print(textFiles)

def main():
    #First, construct a corpus vocab
    corpusDict = {}
    corpusTokens = 0

    for textFile in textFiles:
        thisFile = open(textFile)
        thisText = thisFile.read().lower()
        #remove all but the words
        cleanedText = re.sub(r"[^a-zA-Z0-9]", " ", thisText)
        textWords = words(cleanedText)
        for word in textWords:
            corpusTokens += word[1]
            if word[0] in corpusDict:
                corpusDict[word[0]] += word[1]
            else:
                corpusDict[word[0]] = word[1]
        
    print("Tokens: " + str(corpusTokens), "Types: " + str(len(corpusDict.keys())), "Lower: " + lower, "Upper: " + upper)



def words(text) -> list:
    wordDict = {}
    #Look at each word
    splitText = text.split()
    #create list of all words
    for word in splitText:
        if word not in wordDict:
            wordDict[word] = 1
        else:
            wordDict[word] += 1            
    #next, we sort the dictionary
    sortedWordList = sorted(wordDict, key = wordDict.get, reverse=True)
    sortedWordDict = {}
    for y in sortedWordList:
        sortedWordDict[y]=wordDict[y]
    sortedItems = list(sortedWordDict.items())
    return sortedItems[::-1]

main()