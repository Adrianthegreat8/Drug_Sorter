#module writer

"""
Tools for taking files and creating lists from them
"""

def array_split(_file):
    "splits a file into a list of lists using each line as a row "
    with open(_file, 'r') as myfile:
        lines = myfile.readlines()
        L = [element.strip() for element in lines]

    return L

def array_cut(list, column, sepparator=' '):
    "creates a new list of elements using a specified sepparator and index or 'column'"
    L = [i.split(sepparator)[column] for i in list]
    return L

def main():
    "Test function"
    import os

    os.makedirs('test', exist_ok=True)

    with open('test/testfile.dat', 'w') as myfile:
        myfile.write('AZ,10\nCO,30\nNM,80\n')

    print('test block')
    file_to_use = 'test/testfile.dat'
    cleanlist=array_split(file_to_use)
    print(cleanlist)
    print(array_cut(cleanlist, 1, ','))

if __name__ == '__main__':
    main()