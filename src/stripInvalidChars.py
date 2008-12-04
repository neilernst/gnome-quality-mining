import re

def stripNonValidXMLCharacters(file):
    """ 
    This method ensures that the output String has only
    valid XML unicode characters as specified by the
     XML 1.0 standard. For reference, please see
     <a href="http://www.w3.org/TR/2000/REC-xml-20001006#NT-Char">the
     standard</a>. This method will return an empty
    String if the input is null or empty.
    """
    out = '' # Used to hold the output.
    current = '' # Used to reference the current character.
    if (file == None):
        return "" # vacancy test.
       
    for input in file:
        # encode as hex
        body = input
        #print body
        body=re.compile("[\x01-\x08\x0B\x0C\x0E-\x1F]").sub("*",body)
        #return body
        out = out + body
    #print out
    return out
#        input = input.encode("hex")
        #print input
#        for current in input:
#            if ((current == 0x9) or (current == 0xA) or (current == 0xD) or
#                ((current >= 0x20) and (current <= 0xD7FF)) or
#                ((current >= 0xE000) and (current <= 0xFFFD)) or
#                ((current >= 0x10000) and (current <= 0x10FFFF))):
#                out = out + current
#                print out.decode("hex")
##    return out.decode('hex')
