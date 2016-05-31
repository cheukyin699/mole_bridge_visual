import csv
import re

elements = {}
r_elem_finder = re.compile('[A-Z][a-z]?|[0-9]+')

def init():
    '''
    Initialized elements map with csv values from file
    '''
    global elements
    with open("elements.csv", 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                elements[row[1][1:]] = float(row[3])
            except:
                pass

def getMolarMass(s):
    '''
    Finds the molar mass of an element or a compound
    '''
    molar_mass = 0
    elem_list = re.findall(r_elem_finder, s)

    for i in xrange(len(elem_list)):
        elem = elem_list[i]
        next_elem = elem_list[(i+1) % len(elem_list)]
        multiple = 1

        if elem.isdigit(): continue
        if next_elem.isdigit():
            # Multiply by that many times
            multiple = int(next_elem)

        try:
            molar_mass += elements[elem] * multiple
        except:
            return None

    return molar_mass

# For testing purposes
if __name__ == '__main__':
    init()
    print elements['Ru']
    print getMolarMass('C6')
    print getMolarMass('C6H8O6')
    print getMolarMass('H2O')
