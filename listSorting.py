#!/usr/bin/python

# see: CSchallenge.docx


# imports:

from sys import argv
import re

# function definitions:


def is_integer(string):
    '''
    Checks if a string holds an integer.

    Examples:

    >>> is_integer('12')
    True
    >>> is_integer('12.3')
    False
    >>> is_integer('monkey')
    False
    '''
    try:
        int(string)
        return True
    except ValueError:
        return False


def convert_to_cleaned_words_list(string):
    '''
    This takes a string as input and processes it into words:
    -each word is an integer (+ or -), or a character string
    -the delimiters for words are blank spaces.
    -non-digit and non-alphabetical characters are removed

    Example:

    >>> string = '2-0  cat bi?rd -12 do-@g'
    >>> out = convert_to_cleaned_words_list(string)
    >>> out == ['20', 'cat', 'bird', '-12', 'dog']
    True

    '''

    # chomp off any newlines or white spaces at ends:
    string = string.rstrip()
    string = string.lstrip()

    # remove ascii, & keep numbers, letters, and -'s:
    throwawaychars = re.compile(r'[^\w\s\-]+')
    string = throwawaychars.sub('', string)

    # remove '.'s that are inside of numbers (but not words)?:
    # need to modify the ascii line as well..

    # remove -'s within all words (but keep those in the front):
    string = re.sub(r'([^\s])[\-]+', r'\1', string)

    # combine multiple whitespaces between words into a single space:
    multiplespaces = re.compile(r'[\s]+')
    string = multiplespaces.sub(' ', string)

    # split into words:
    words = string.split(' ')

    # remove '-'s from start of words, if words are not integers:
    for ind, word in enumerate(words):
        if not is_integer(word):
            word = re.sub(r'[\-]+', '', word)
            words[ind] = word

    return words


def insert_sublist(mainList, subInds, subList):
    '''
    take a sublist, which has a partner list of indices from
    mainlist, and insert the sublist into the mainlist at the
    indices defined in subInds (overwriting anything in mainList
    in those indices previously).

    Example:

    >>> mL = ['b','a','1','3']
    >>> sI = [0,1]
    >>> sL = ['B','A']
    >>> insert_sublist(mL, sI, sL) == ['B', 'A', '1', '3']
    True

    '''
    for n in range(len(subInds)):
        currInd = subInds[n]
        currVal = subList[n]
        mainList[currInd] = currVal

    return mainList


def performListSorting(data):
    '''
    This is the function that does the heavy lifting, and calls
    the other functions.
    It takes in a string and processes it into words:
    -each word is an integer (+ or -), or a character string
    -the delimiters for words are blank spaces.
    -non-digit and non-alphabetical characters are removed

    Then, it produces a new string, where the chars are sorted
    and the ints are sorted within their original indices.

    Example:

    >>> data = ' 2-0 ca-t -bi?rd -12 do@g bla72a 124 monkey '
    >>> dataout = performListSorting(data)
    >>> dataout == '-12 bird bla72a 20 cat dog 124 monkey'
    True

    '''
    # process data:
    words = convert_to_cleaned_words_list(data)

    # create position lists & member lists for ints and strings:
    stringInds = []
    intInds = []
    strings = []
    ints = []
    for ind, word in enumerate(words):
        if is_integer(word):
            ints.append(word)
            intInds.append(ind)
        else:
            strings.append(word)
            stringInds.append(ind)

    # sort the lists of strings and ints:
    strings.sort()
    ints.sort(key=int)

    # recombine the ints and strings structures according to inds:
    # note, inds are already sorted! (also, this is a merge operation)
    # reinitialize words again as all nulls, and then check @ end?
    words = insert_sublist(words, stringInds, strings)
    words = insert_sublist(words, intInds, ints)
    dataout = ' '.join(words)

    return dataout

#############################
# main function starts here #
#############################


def main():
    '''

    '''

    # grab command line inputs:
    script, filein, fileout = argv

    # read in file:
    with open(filein) as f:
        data = f.read()

    # do the list sorting:
    dataout = performListSorting(data)

    # write to file:
    with open(fileout, "w") as fout:
        fout.write(dataout)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
