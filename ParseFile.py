#!/usr/bin/env python

# This file is part of PyPop

# Copyright (C) 2003. The Regents of the University of California (Regents)
# All Rights Reserved.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

# REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING
# DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS
# IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
# UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

"""Module for parsing data files.

   Includes classes for parsing individuals genotyped at multiple loci
   and classes for parsing literature data which only includes allele
   counts."""

import sys, os, string, types, re

from Utils import getStreamType, StringMatrix, OrderedDict, TextOutputStream

class ParseFile:
    """*Abstract* class for parsing a datafile.

    *Not to be instantiated.*"""
    def __init__(self,
                 filename,
                 validPopFields=None,
                 validSampleFields=None,
                 separator='\t',
                 fieldPairDesignator='_1:_2',
                 alleleDesignator='*',
                 popNameDesignator='+',
                 debug=0):
        """Constructor for ParseFile object.

        - 'filename': filename for the file to be parsed.

        - 'validPopFields': a string consisting of valid headers (one
           per line) for overall population data (no default)

        - 'validSampleFields': a string consisting of valid headers
           (one per line) for lines of sample data.  (no default)

        - 'separator': separator for adjacent fields (default: a tab
           stop, '\\t').

        - 'fieldPairDesignator': a string which consists of additions
          to the allele `stem' for fields grouped in pairs (allele
          fields) [e.g. for `HLA-A', and `HLA-A(2)', then we use
          ':(2)', for `DQA1_1' and `DQA1_2', then use use '_1:_2', the
          latter case distinguishes both fields from the stem]
          (default: ':(2)')

        - 'alleleDesignator': The first character of the key which
        determines whether this column contains allele data.  Defaults to
        '*'

        - 'popNameDesignator': The first character of the key which
        determines whether this column contains the population name.
        Defaults to '+'

        - 'debug': Switches debugging on if set to '1' (default: no
          debugging, '0')"""

        self.filename = filename
        self.validPopFields=validPopFields
        self.validSampleFields=validSampleFields
        self.debug = debug
        self.separator = separator
        self.fieldPairDesignator = fieldPairDesignator
        self.alleleDesignator=alleleDesignator
        self.popNameDesignator = popNameDesignator

        self.popFields = ParseFile._dbFieldsRead(self,self.validPopFields)
        self.sampleFields = ParseFile._dbFieldsRead(self,self.validSampleFields)
        if self.debug:
            # debugging only
            print self.popFields
            print self.sampleFields

        # Reads and parses a given filename.
        
        self._sampleFileRead(self.filename)
        self._mapPopHeaders()
        self._mapSampleHeaders()

    def _dbFieldsRead(self, data):
        """Reads the valid key, value pairs.

        Takes a string that is expected to consist of database field
        names separated by newlines.

        Returns a tuple of field names.

        *For internal use only.*"""
        li = []
        for line in string.split(data, os.linesep):
            if self.debug:
                print string.rstrip(line)
            li.append(string.rstrip(line))
        return tuple(li)

    def _mapFields(self, line, fieldList):
        """Creates a list of valid database fields.

        From a separator delimited string, creates a list of valid
        fields and creates a dictionary of positions keyed by valid
        field names.

        - Complains if a field name is not valid.

        - Complains if the correct number of fields are not found for
        the metadata headers.
        
        Returns a 2-tuple:
        
        - a dictionary keyed by field name.

        - the total number of  metadata fields.

        *For internal use only.*"""

        # split line
        fields = line.split(self.separator)

        # check to see if the correct number of fields found
        if len(fields) != len(fieldList):
            print "error: found", len(fields), "fields expected", \
                  len(fieldList), "fields"
        
        i = 0
        assoc = OrderedDict()
        for field in fields:

            # strip the field of leading and trailing blanks because
            # column name may inadvertantly contain these due to
            # spreadsheet -> tab-delimited file format idiosyncrasies
        
            field = string.strip(field)

            # check to see whether field is a valid key, and generate
            # the appropriate identifier, this is done as method call
            # so it can overwritten in subclasses of this abstract
            # class (i.e. the subclass will have 'knowledge' about the
            # nature of fields, but not this abstract class)
            
            isValidKey, key = self.genValidKey(field, fieldList)

            if isValidKey:

                # if key is one of pair already in map, add it to make
                # a tuple at that key e.g. `HLA-A(2)' already exists
                # and inserting `HLA-A', or `DQB1_1' and `DQB1_2' should
                # both be inserted at `DQB1'

                if assoc.has_key(key):
                    assoc[key] = assoc[key], i
                else:
                   assoc[key] = i
                    
            else:
                print "error: field name `%s' not valid" % field

            i = i + 1

        return assoc, i

    def _sampleFileRead(self, filename):
        """Reads filename into object.

        Takes a filename and reads the file data into an instance variable.

        *For internal use only*.
        """
        f = open(filename, 'r')
        self.fileData = f.readlines()

    def _mapPopHeaders(self):

        """Create associations for field names and input columns.
        
        Using the header information from the top of the file, creates
        a dictionary for the population-level data.

        Also validates the file information for the correct number of fields
        are present on each line

        *For internal use only*."""

        # get population header metadata
        popHeaderLine = string.rstrip(self.fileData[0])

        # parse it
        self.popMap, fieldCount = self._mapFields(popHeaderLine, self.popFields)

        # debugging only
        if self.debug:
            print "population header line: ", popHeaderLine
            print self.popMap

        # get population data
        popDataLine = string.rstrip(self.fileData[1])
        # debugging only
        if self.debug:
            print "population data line: ", popDataLine

        # make sure pop data line matches number expected from metadata
        popDataFields = string.split(popDataLine, self.separator)
        if len(popDataFields) != fieldCount:
            print "error: found", len(popDataFields),\
                  "fields expected", fieldCount, "fields"

        # create a dictionary using the metadata field names as key
        # for the population data
        self.popData = OrderedDict()
        for popField in self.popMap.keys():
            self.popData[popField] = popDataFields[self.popMap[popField]]

    def _mapSampleHeaders(self):
        """Create the associations between field names and input columns.

        Using the header information from the top of the file, creates
        associations for the sample data fields.

        Also validates the file information for the correct number of fields
        are present on each line

        *For internal use only*."""

        # get sample header metadata
        sampleHeaderLine = string.rstrip(self.fileData[2])

        # parse it
        self.sampleMap, fieldCount = self._mapFields(sampleHeaderLine,
                                                     self.sampleFields)
        # debugging only
        if self.debug:
            print "sample header line: ", sampleHeaderLine
            print self.sampleMap

        # check file data to see that correct number of fields are
        # present for each sample

        for lineCount in range(3, len(self.fileData)):

            # retrieve and strip newline
            line = string.rstrip(self.fileData[lineCount])

            # restore the data with the newline stripped
            self.fileData[lineCount] = line
            
            fields = string.split(line, self.separator)
            if fieldCount != len(fields):
                print "error: incorrect number of fields:", len(fields), \
                      "found, should have:", fieldCount, \
                      "\noffending line is:\n", line


    def getPopData(self):
        """Returns a dictionary of population data.

        Dictionary is keyed by types specified in population metadata
        file"""
        return self.popData

    def getSampleMap(self):
        """Returns dictionary of sample data.

        Each dictionary position contains either a 2-tuple of column
        position or a single column position keyed by field originally
        specified in sample metadata file"""

        return self.sampleMap

    def getFileData(self):
        """Returns file data.

        Returns a 2-tuple `wrapper':

        - raw sample lines, *without*  header metadata.
        
        - the field separator."""
        return self.fileData[3:], self.separator
    
    def genSampleOutput(self, fieldList):
        """Prints the data specified in ordered field list.

        *Use is currently deprecated.*"""

        #for field in fieldList:
        #print string.strip(field) + self.separator,
        for lineCount in range(3, len(self.fileData)):
            line = string.strip(self.fileData[lineCount])
            element = string.split(line, self.separator)
            for field in fieldList:
                if self.sampleMap.has_key(field):
                    print element[self.sampleMap[field]],
                else:
                    print "can't find this field"
                    print "\n"

    def serializeMetadataTo(self, stream):
        type = getStreamType(stream)
        stream.opentag('populationdata')
        stream.writeln()

        for summary in self.popData.keys():
            # convert metadata name into a XML tag name
            tagname = string.lower(string.replace(summary,' ','-'))
            stream.tagContents(tagname, self.popData[summary])
            stream.writeln()

        # call subclass-specific metadata serialization
        self.serializeSubclassMetadataTo(stream)
        
        stream.closetag('populationdata')
        stream.writeln()


class ParseGenotypeFile(ParseFile):
    """Class to parse standard datafile in genotype form."""
    
    def __init__(self,
                 filename,
                 untypedAllele='****',
                 **kw):
        """Constructor for ParseGenotypeFile.

        - 'filename': filename for the file to be parsed.
        
        In addition to the arguments for the base class, this class
        accepts the following additional keywords:

        - 'untypedAllele': The designator for an untyped locus.  Defaults
        to '****'.
        """
        self.untypedAllele=untypedAllele
        
        ParseFile.__init__(self, filename, **kw)

        self._genDataStructures()

    def _genInternalMaps(self):
        """Returns dictionary containing 2-tuple of column position.

        It is keyed by locus names originally specified in sample
        metadata file, the locus names (keys) are made uppercase and
        don't contain the allele designator.

        Note that this is simply a transformed _subset_ of that
        returned by **getSampleMap()**

        *For internal use only.*"""

        self.alleleMap = OrderedDict()
        for key in self.sampleMap.keys():

            # do we have the allele designator?
            if key[0] == self.alleleDesignator:
                # remove allele designator, only necessary
                # for initial splitting out of locus keys from
                # other fields, and also make uppercase
                locusKey = string.upper(key[len(self.alleleDesignator):])
                self.alleleMap[locusKey] = self.sampleMap[key]
            elif key[0] == self.popNameDesignator:
                self.popNameCol = self.sampleMap[key]

        # save population name
        self.popName = string.split(self.fileData[3], self.separator)[self.popNameCol]

        return self.alleleMap

    def _genDataStructures(self):
        """Generates matrix only
        
        *For internal use only.*"""        

        # generate alleleMap and population field name
        self._genInternalMaps()

        sampleDataLines, separator = self.getFileData()

        if self.debug:
            print 'sampleMap keys:', self.sampleMap.keys()
            print 'sampleMap values:', self.sampleMap.values()
            print 'first line of data', sampleDataLines[0]


        # then total number of individuals in data file
        self.totalIndivCount = len(sampleDataLines)

        # total number of loci contained in original file
        self.totalLocusCount = len(self.alleleMap)

        # freeze the list of locusKeys in a particular order
        self.locusKeys = self.alleleMap.keys()

        # create an empty-list of lists to store all the row data
        #self.individualsList = [[] for line in range(0, self.totalIndivCount)]
        self.matrix = StringMatrix(self.totalIndivCount, self.locusKeys)

        for locus in self.locusKeys:
            if self.debug:
               print "locus name:", locus
               print "column tuple:", self.alleleMap[locus]

            col1, col2 = self.alleleMap[locus]

            # re-initialise the row count on each iteration of the locus
            rowCount = 0
            for line in sampleDataLines:
                fields = string.split(line, separator)

                # create data structures

                allele1 = string.strip(fields[col1])
                allele2 = string.strip(fields[col2])

                # underlying NumPy array data type won't allow storage
                # of any sequence-type object (e.g. list or tuple) but
                # we can workaround this by overriding the __setitem__
                # method of the UserArray wrapper class used for
                # subtyping and storing tuple internally as two
                # separate columns in the underlying array.

                self.matrix[rowCount,locus] = (allele1, allele2)
                
                if self.debug:
                    print rowCount, self.matrix[rowCount,locus]

                # increment row count
                rowCount += 1

    def genValidKey(self, field, fieldList):
        """Check and validate key.

        - 'field':  string with field name.

        - 'fieldList':  a dictionary of valid fields.
        
        Check to see whether 'field' is a valid key, and generate the
        appropriate 'key'.  Returns a 2-tuple consisting of
        'isValidKey' boolean and the 'key'.

        *Note: this is explicitly done in the subclass of the abstract
        'ParseFile' class (i.e. since this subclass should have
        `knowledge' about the nature of fields, but the abstract
        class should not have)*"""

        if (field in fieldList) or \
           (self.alleleDesignator + field in fieldList):
            isValidKey = 1
        else:
            if self.popNameDesignator + field in fieldList:
                isValidKey = 1
            else:
                isValidKey = 0

        # generate the key that matches the one in the data file
        # format

        # if this is an `allele'-type field
        if self.alleleDesignator + field in fieldList:

            li = string.split(self.fieldPairDesignator,":")

            # if pair identifiers are both the same length and
            # non-zero (e.g. '_1' and '_2', then we can assume that
            # the underlying `stem' should be the field name with the
            # pair identifer stripped off, otherwise simply use the
            # field name
            
            if (len(li[0]) == len(li[1])) and (len(li[0]) != 0):
                key = self.alleleDesignator + field[:-len(li[0])]
            else:
                key = self.alleleDesignator + field

        else:
            # this is the population field name
            if self.popNameDesignator + field in fieldList:
                key = self.popNameDesignator + field
            else:
                # this is a regular (non-`allele' type field)
                key = field

        if self.debug:
            print "validKey: %d, key: %s" % (isValidKey, key)
            
        return isValidKey, key

    def getMatrix(self):
        """Returns the genotype data.

        Returns the genotype data in a 'StringMatrix' NumPy array.
        """
        return self.matrix

    def serializeSubclassMetadataTo(self, stream):
        """Serialize subclass-specific metadata."""

        # output population name first
        stream.tagContents('popname', self.popName)
        stream.writeln()


class ParseAlleleCountFile(ParseFile):
    """Class to parse datafile in allele count form.

    Currently  only handles one locus per population, in format:

    <metadata-line1>
    <metadata-line2>
    DQA1 count
    0102 20
    0103 33
    ...
    
    *Currently a prototype implementation*."""
    def __init__(self,
                 filename,
                 **kw):
        ParseFile.__init__(self, filename, **kw)
        self._genDataStructures()

    def _genDataStructures(self):
        sampleDataLines, separator = self.getFileData()

        self.alleleTable = {}
        
        for line in sampleDataLines:
            allele, count = string.split(line, separator)
            # store as an integer
            self.alleleTable[allele] = int(count)

        if self.debug:
            print 'alleleTable', self.alleleTable
            print 'sampleMap keys:', self.sampleMap.keys()
            print 'sampleMap values:', self.sampleMap.values()
            
        self.locusName = self.sampleMap.keys()[0]
        

    def genValidKey(self, field, fieldList):
        """Checks to  see validity of a field.

        Given a 'field', this is checked against the 'fieldList' and a
        tuple of a boolean (key is valid) and a a key is returned.

        The first element in the 'fieldList' which is a locus name,
        can match one of many loci (delimited by colons ':').  E.g. it
        may look like:

        'DQA1:DRA:DQB1'

        If the field in the input file match *any* of these keys,
        return the field and a valid match.
        """
        if (field in fieldList):
            isValidKey = 1
        else:
            # get the locus name, always the first in the list
            name = fieldList[0]

            # turn this into a list, splitting on the colon
            # delimiter
            listOfValidLoci = string.split(name, ":")

            # check to see if the locus is one of the valid ones
            if (field in listOfValidLoci):
                isValidKey = 1
            else:
                isValidKey = 0

        return isValidKey, field

    def serializeSubclassMetadataTo(self, stream):
        # nothing special is required here, so pass
        pass
    
    def getAlleleTable(self):
        return self.alleleTable

    def getLocusName(self):
        # the first key is the name of the locus
        return self.locusName

# this test harness is called if this module is executed standalone
if __name__ == "__main__":

    print "dummy test harness, currently a no-op"
    #parsefile = ParseGenotypeFile(sys.argv[1], debug=1)


