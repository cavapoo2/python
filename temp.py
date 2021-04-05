def matchers():
    return {'user account hardening': (4),
            'authentication policy': (2),
            'system hardening': (4),
            'windows defender configuration': (4),
            'applocker configuration': (4),
            'bitlocker configuration': (4),
            'windows defender exploit guard configuration': (4),
            'Windows Defender Device Guard and Application Control configuration':(4),
            'Windows Defender Application Guard configuration':(4),
            'Windows Defender Firewall configuration':(4)}



def string_pos(str):
    return str.find(str)

def match_heading_with_all_line_numbers(stringlist,headings):
    # create dictionary with headings as keys
    d = dict((heading.lower(), []) for heading in headings)
    line_number = 0
    for line in stringlist:
        for heading in headings:
            if line.lower().find(heading.lower()) > -1:
                # append line number to map list
                d[heading.lower()].append(line_number)
        line_number += 1
    return d

'''
#take n items from a dictionary list given the key and number
of items to take. if n is too large then just takes the
next size down.
'''
def take_n_from_map_list(dic, key, n, start):
    vals = dic[key]
    return vals[start:(start + n)]

def take_n_from_list(thelist, start, n):
    return thelist[start:(start + n)]

'''
Finds a string in a string list start from
list index i1 to list index i2.
in this case we use this to find the 
group policy header
'''
def find_string(stringlist, strtofind, i1, i2):
    #search between each possible position 
    r = list(range(i1, i2+1))
    for i in r:
        if stringlist[i].lower().find(strtofind.lower()) > -1:
            return True
    return False

'''
Find a group policy in the string list starting
from list index i1 to list index i2
Pattern in this case is string > string > ..
'''
def find_group_policy(stringlist, i1, i2, pass_rate, delim):
    #search between each possible postion
    r = list(range(i1, i2+1))
    for i in r:
        if stringlist[i].count(delim) >= pass_rate:
            return i
    # -1 indicates not found
    return -1

#def get_group

'''
for each possible heading position look
ahead to check for group policy settings header exists.
if so then this is the position where the group policies
will actually start.
'''
def get_exact_group_policy_position(stringlist, possible_positions):
    res = []
    headings = possible_positions.keys()
    #last index
    maxi = len(stringlist)-1
    for heading in headings:
        positions = possible_positions[heading]
        #create an additional last index for last max search position
        #50 is enough of estimate to cover line look ahead limit   
        positions.append(min(positions[-1] + 50, maxi))
        p1 = 0
        p2 = 0
        for i in range(len(positions)-1):
            r = take_n_from_list(positions, i, 2)
            p1 = find_string(stringlist,'Group Policy',r[0],r[1])
            p2 = find_group_policy(stringlist,r[0],r[1],2,'>')
        if p1 and p2 > -1:
            res.append((heading, p2))

    return res

def all_except(lst,not_this):
    res = []
    for i in lst:
        if i.lower() != not_this.lower():
            res.append(i)
    return res

'''
gets all headings from tuple list
'''

def get_all_headings(matchers):
    res=[]
    for m in matchers:
        res.append(m[0])

    return res

'''
checks if string matches any in the list of strings
'''
def contains(s, str_list):
    for a in str_list:
        if s.lower() == a.lower():
            return True
    return False
'''
checks if any items in lst
are in str_list. if so drop 
them from the list
'''
def drop(lst, str_list):
    res = []
    for l in lst:
        found = False
        for s in str_list:
            if s == l:
                found = True
        if found == False:
            res.append(l)
    return res



def get_each_policy(stringlist, matchers):
    res= []
    for m in matchers:
        header = m[0]
        delim_count = m[1] #match at least this number of delims
        ignores = m[2] #ignore if line contains this

def is_heading_line(line, headings):
    for h in headings:
        if h.lower().strip() == line.lower().strip():
            return (h,True)
    
    return ('',False)

def line_does_not_contain_any(line,ok,nok):


def main():

    ncsc = ""
    wiki = ""
    headings = ['User account hardening', 'Authentication policy']
    with open('ncsc.txt', 'r') as file:
        ncsc = file.read().split('\n')

    headings = matchers().keys()
    maxlen = len(ncsc)
    rng = list(range(0,maxlen))
    for i in rng:
        line = ncsc[i]
        #check if line is a heading
        resh = is_heading_line(line,headings)
        if resh[1]:
            #current heading of interest
            current_heading = resh[0]
            #get all headings except the current heading
            not_current_heading = drop(current_heading,headings)




    
    # add wiki read here
    # get a map of line numbers that match the headings
    #p = match_heading_with_all_line_numbers(ncsc, headings)
    # for each possible line number determine which
    # one contains the group policy heading and 
    #group policy settings. 
    #print(p)
    #e = get_exact_group_policy_position(ncsc, p)
    #print(e)



if __name__ == "__main__":
    main()
