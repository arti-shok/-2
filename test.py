with open("text_level3.txt", "r", encoding= 'utf8') as f:
    l = f.readlines()
    r = [i.strip() for i in l]
print(r)