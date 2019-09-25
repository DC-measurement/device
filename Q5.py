f = open('writeme.xlsx', 'w')

f.write('1st ')
f.write("line\n")
f.writelines(['2nd line\n', 'last line'])

f.close()

f = open('writeme.xlsx', 'r')
for s in f:
    print(s)
f.close()

f = open('writeme.xlsx', 'w')

f.write('2: 1st line\n')
f.write('2: 2nd line\n')
f.write('2: last line\n')

f.close()

print('-----------')
f = open('writeme.xlsx', 'r')
for s in f:
    print(s)
f.close()

f = open('writeme.xlsx', 'a')

f.write('3: 1st line\n')
f.write('3: 2nd line\n')
f.write('3: last line\n')

f.close()

print('-----------')
f = open('writeme.xlsx', 'r')
for s in f:
    print(s)
f.close()