# IMPORTS
import os
import json
import groupingTOC as GTOC
import helper_functions as hf
import time

global_toc = GTOC.preload_toc()
reverse_index_cache = {}


def process_query(query: str): #NEW
    start_time = time.time()
    """
    Uses the given AND boolean query in order to search for the top 5 related URLs.
    Returns a list of the top URLs.

    input:
        query: string -> the user query
    output:
        list -> top URLs
    """

    temp_tokens = query.split()
    tokens = []
    for t in temp_tokens:
        t = t.translate(hf.punctuation_table)
        t = t.lower()
        t = hf.porter_stemmer(t)
        if t not in tokens and len(tokens) <= 20:
            tokens.append(t)

    
    listOlists = []
    
    start_time1 = time.time()
    for token in tokens:

        tokenPostings = retrieve_tokenPostings(token, global_toc)
        if(tokenPostings!=[] and tokenPostings is not None):
            listOlists.append(tokenPostings)

    end_time2 = time.time()
    print(f"Time taken by retrieve_tokenPostings: {end_time2 - start_time1} seconds")
    

    start_timemerge = time.time()

    listOlists.sort(key=len,reverse=True)

    if(len(listOlists)>0):
        mergedList = listOlists[-1][:min(100,len(listOlists[-1]))]
        listOlists.pop()

        for list in reversed(listOlists):
            templist = list[:min(len(list),100)]
            mergedList = intersect_sorted_lists(mergedList,templist)

        sorted_data = sorted(mergedList, key=lambda x: x[1][0], reverse=True)#THIS SORTS THE LIST BASED ON CUMLULITIVE TF-IDF
        urlOffsets=[item[0] for item in sorted_data] #GET THE DOCID on the list

        end_timemerge = time.time()
        print(f"Time taken by merge: {end_timemerge - start_timemerge} seconds")
        end_time = time.time()
        print(f"Total Time taken: {end_time - start_time} seconds")
        return getURLs(urlOffsets), (end_time - start_time)
        

    else:
        return[]

def intersect_sorted_lists(list1, list2):
    i, j = 0, 0
    merged_result = []

    while i < len(list1) and j < len(list2):
        key1, value1 = list1[i]
        key2, value2 = list2[j]

        key1_int = int(key1)
        key2_int = int(key2)

        if key1_int < key2_int:
            merged_result.append(list1[i])
            i += 1
        elif key1_int > key2_int:
            merged_result.append(list2[j])
            j += 1
        else:

            merged_value = [
                value1[0] + value2[0], 
                set(value1[1]).union(value2[1])  
            ]
            merged_result.append([key1, merged_value])
            i += 1
            j += 1

    if i < len(list1):
        merged_result.extend(list1[i:])
    if j < len(list2):
        merged_result.extend(list2[j:])

    return merged_result


def retrieve_tokenPostings(token, global_toc):
    reverseIndexFolder="ReverseIndexes"
    charName = token[0].lower()  # Find the designated char and File

    charTOC = global_toc[charName]


    if token not in charTOC:
        return []  # Return empty if token doesn't exist

    # Saves the byte offset
    byteOffset = charTOC[token]

    # Get the postings using offset
    reverseIndexFile = os.path.join(reverseIndexFolder, f"{charName}.txt")
    with open(reverseIndexFile, 'r') as reverseIndex:
        reverseIndex.seek(byteOffset)
        line = reverseIndex.readline()
        line = line.strip()

        # Extract the token and postings
        currToken, postings = line.split(':', 1)
        if currToken == token:
                postings = postings.replace("'", '"').replace("{", "[").replace("}", "]")
                return json.loads(postings) # Convert postings to a Python object

    return []  # Token not found in the file

def getURLs(idList): #NEW
    '''
    Input: Document ID list
    Output: URL list corresponding to docIDs
    '''
    urls = []
    with open("URL_Collective.txt", "rb") as url_collection:
        for offset in idList:
            url_collection.seek(int(offset), 0)
            urls.append(url_collection.readline())
    return urls

if __name__ == "__main__":
    pass
