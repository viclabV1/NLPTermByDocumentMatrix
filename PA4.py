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
import numpy as np
#Get arguments
lower = int(sys.argv[1])
upper = int(sys.argv[2])
textFiles = sys.argv[3:]
print(textFiles)

def main():
    #First, construct a corpus vocab
    corpusList = []
    corpusDict = {}
    corpusTokens = 0

    #Create a dict of all words in the corpus
    for textFile in textFiles:
        thisFile = open(textFile)
        thisText = thisFile.read().lower()
        thisFile.close()
        #remove all but the words
        cleanedText = re.sub(r"[^a-zA-Z0-9]", " ", thisText)
        textWords = words(cleanedText).items()
        for word in textWords:
            corpusTokens += word[1]
            if word[0] not in corpusDict:
                corpusDict[word[0]]=word[1]
            else:
                corpusDict[word[0]]+=word[1]
    #Next create a list of all words that fit within cutoff
    for word in corpusDict:
        if corpusDict[word] <= upper and corpusDict[word] >= lower:
            corpusList.append(word)
        
    corpusList.sort()
    
    #Now, look at each text and get word frequencies (not the most efficient way to do this,
    # but easy to implement)
    occurrences = []
    for textFile in textFiles:
        occurrenceList = []
        thisFile = open(textFile)
        thisText = thisFile.read().lower()
        thisFile.close()
        cleanedText = re.sub(r"[^a-zA-Z0-9]", " ", thisText)
        textWords = words(cleanedText)
        for word in corpusList:
            if word in textWords:
                occurrenceList.append(textWords[word])
            else:
                occurrenceList.append(0)
        occurrenceTuple = (textFile, occurrenceList)
        occurrences.append(occurrenceTuple)
    
    #Finally, we will make a new list consisting of all cosine similarity
    #values.
    cosineList = []
    #comparisons only need be done once
    for i in range(0,len(occurrences)):
        for j in range(i, len(occurrences)):
            array1, array2 = np.array(occurrences[i][1]), np.array(occurrences[j][1])
            #get dot product and magnitude
            thisDot = np.dot(array1, array2)
            mag1, mag2 = np.linalg.norm(array1), np.linalg.norm(array2)
            #cos = (a.b)/(|a||b|)
            thisCos = thisDot/(mag1 * mag2)
            thisComp = occurrences[i][0] + "\t" + occurrences[j][0] + "\t"
            cosTuple = (thisComp, thisCos)
            cosineList.append(cosTuple)
    cosineList.sort(key = lambda x: x[1], reverse=True) 
    #Finally, print everything
    print("Tokens: " + str(corpusTokens), "Types: " + str(len(corpusList)), "Lower: " + str(lower), "Upper: " + str(upper))
    for element in cosineList:
        print(element[0],element[1])

        


    

    


#function to get word frequency in a given text
def words(text) -> dict:
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
    return sortedWordDict

main()