with open('../big-dataset/old-texts/old-texts-clean-tashkeel/أحكام\ القرآن\ للجصاص.txt ') as f:
	l = f.readlines()

s = ''

for line in l:
	s += line

s = set(s)
print(len(s))

for x in s:
	print(x)
