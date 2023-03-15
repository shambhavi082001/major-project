

import re

# for validating an email

#def check(email):
   # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #if (re.search(regex,email)):
       # return True
    #return False


    # for validating an Email
def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
    if(re.fullmatch(regex, email)):
        return True
    return False