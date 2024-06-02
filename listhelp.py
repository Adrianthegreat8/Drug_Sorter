L = ['AZ,10','NY,20','NM,30','CA,40']
L1 = [['AZ',10], ['NY',20], ['NM',30], ['CA',40]]


print(L)
print(type(L),'\n')

print(L[0])
print(type(L[0]))

L[0] = L[0].split(',')

print(len(L[0]))

L1[0] = ['AZ',10]

print(type(L[0]))