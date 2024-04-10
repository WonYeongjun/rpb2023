import numpy as np
import matplotlib.pyplot as plt
# Load the 8x8 binary image from the CSV file
image = np.loadtxt("square.csv", delimiter=",")
# Ensure the loaded data is of integer type for display
image = image.astype(int)
# Display the image
plt.imshow(image)
plt.title('8x8 Binary Image with Random Pixel Values')
plt.show()
