import numpy as np

# Load the 8x8 binary image from the CSV file
image = np.loadtxt("square.csv", delimiter=",")
# Ensure the loaded data is of integer type for display
image = image.astype(int)
blacklist=[]
for y in range(image.shape[0]):
	for x in range(image.shape[1]):
		if image[y, x] == 0:
			print("(%d,%d)" % (x,y))
			blacklist.append((x,y))
print(len(blacklist))
