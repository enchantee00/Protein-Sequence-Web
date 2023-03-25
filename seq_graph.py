import matplotlib.pyplot as plt

file = open("TextFile.txt", "r")
sequence = file.read()
file.close()
print(sequence)


# single amino acid
charge = []

# multiple amino acid
common = []
diff = []
sequential_charge = []


for i in sequence:
    if i == 'D' or i == 'E':
        charge.append(-1)
    elif i == 'K' or i == 'R':
        charge.append(1)
    elif i == 'H':
        charge.append(0.1)
    else:
        charge.append(0)

plt.plot(range(len(sequence)),charge)
plt.xticks(range(len(sequence)), list(sequence), fontsize = 5)
# plt.xticks(list(sequence))
plt.show()