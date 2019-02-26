#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 17:25:21 2018

@author: jessicaking
"""

# Strings and Counting:
# A Public Library would like to institute a new book identifi-
# cation system. This identification system would be a unique local identified for each book
#
# in their catalogue. The identifier for each book should satisfy the following
# (a) Each book has a unique identifier
# (b) A portion of the identifier contains information about publication year
# (c) A portion of the identifier contains information about the item collection
# (d) 8 characters must be used for the identifier
# (e) Characters must be numbers or letters
# (f) Characters must have characteristically distinct.
# For instance 0 and O, I and l, v and u are all pairs that are not characteristically
# distinct
# (g) The identifier should not be case sensitive
# (h) Enable the library to expand its catalogue to 1 million books and expand its number
# of item collections
# Use the catalogue located on canvas to construct this new identification system. Be sure to
# discuss your process at each step, justify your reasoning, provide a key for the identifiers,
# and the process for expansion.


# needs to implement 2 apis
# 1.insertBook() input a book and out put it's id
# 2.getBook() input a id and output a book

import xlrd
import re

# the book class
class Book:
    def __init__(self, title, author, isbn, publicationYear, publisher, itemCollection, itemCount):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publicationYear = publicationYear
        self.publisher = publisher
        self.itemCollection = itemCollection
        self.itemCount = int(itemCount)

    def __repr__(self):
        return "title: " + self.title + '\n' \
               + "author: " + author + '\n' \
               + "publicationYear: " + str(self.publicationYear) + '\n' \
               + "publisher: " + self.publisher + '\n'\
               + "itemCollection: " + self.itemCollection + '\n' \
               + "itemCount: " + str(self.itemCount)


class BookSystem:
    # num of books
    count = 0

    # char set used to code id
    charSet = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z']

    charSize = len(charSet)

    # starting year
    yearStart = 1600

    # all item collections
    dictItemCollection = {}

    # all books
    dictBook = {}

    # Per requirement, the generated id should be 8 digits for now
    # which now designates 5 for counting books, 2 for counting years, 1 for counting ItemCollections
    # these values can be change when needed
    countDigits = 5
    yearDigits = 2
    itemCollectionDigits = 1

    # Given a book, store it into system
    # returns the encoded Id
    def insertBook(self, book):
        id = self.generateId(book)
        self.dictBook[id] = book
        return id

    # Given a encoded id
    # returns the book
    def getBook(self, id):
        id = id.upper()
        if id in self.dictBook:
            return self.dictBook[id]
        return None

    def generateId(self, book):
        encodedCount = self.getEncodedCount();
        encodedYear = self.getEncodedYear(book.publicationYear)
        encodedItemCollection = self.getEncodedItemCollection(book.itemCollection)
        id = encodedCount + encodedYear + encodedItemCollection;
        return id

    def getEncodedCount(self):
        self.count = self.count + 1
        num = self.count
        res = ''
        for i in range(0, self.countDigits):
            curChar = self.charSet[num % self.charSize]
            num = int(num / self.charSize)
            res = curChar + res
        return res

    def getEncodedYear(self, numYear):
        res = ''
        numYear = numYear - self.yearStart
        for i in range(0, self.yearDigits):
            curChar = self.charSet[numYear % self.charSize]
            numYear = int(numYear / self.charSize)
            res = curChar + res
        return res

    def getEncodedItemCollection(self, itemCollection):
        res = ''
        if (itemCollection in self.dictItemCollection):
            index = self.dictItemCollection[itemCollection]
        else:
            index = len(self.dictItemCollection)
            self.dictItemCollection[itemCollection] = index
        for i in range(0, self.itemCollectionDigits):
            curChar = self.charSet[index % self.charSize]
            index = int(index / self.charSize)
            res = curChar + res
        return res



# demo

# location of the xlsx file, needed to be changed to correct file location before running demo
src = "c:\Library_Collection_Inventory.xlsx"

sheet_index = 0

print("Loading excel sheet, please wait......")
excelBook = xlrd.open_workbook(src)
print("Loading excel sheet complete")

workSheet = excelBook.sheet_by_index(sheet_index)
rowStart = 1

# create a new bookSystem
bookSystem = BookSystem()

# extra all book info and stores to the book System
for row in range(1, workSheet.nrows - 1):
    title = workSheet.cell_value(row, 0)
    author = workSheet.cell_value(row, 1)
    isbn = workSheet.cell_value(row, 2)
    publicationYear = workSheet.cell_value(row, 3)
    if isinstance(publicationYear, str):
        publicationYear = ''.join(re.findall('\d+', publicationYear))
    try:
        publicationYear = int(publicationYear)
    except ValueError:
        print("publicationYear can not be parsed! value: " + publicationYear + "row: " + str(row))
        publicationYear = 0
    publisher = workSheet.cell_value(row, 4)
    itemCollection = workSheet.cell_value(row, 5)
    itemCount = workSheet.cell_value(row, 6)
    curBook = Book(title, author, isbn, publicationYear, publisher, itemCollection, itemCount)

    id = bookSystem.insertBook(curBook)
    print("id = " + id)

numOfRows = workSheet.nrows

print(str(numOfRows) + " books were stored in the system")


# test the getBook
print("========Welcome to book System!========")
while True:
    bookId = input("please type in the book id:")
    curBook = bookSystem.getBook(bookId)
    if curBook is None:
        print("The book id is invalid!")
    else:
        print(curBook)
