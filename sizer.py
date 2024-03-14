import cv2 
  
# Load the image 
fname = "image_1.png"
img = cv2.imread(fname) 
  
# Convert the image to grayscale 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# Apply a threshold to the image to 
# separate the objects from the background 
ret, thresh = cv2.threshold( 
    gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) 
  
# Find the contours of the objects in the image 
contours, hierarchy = cv2.findContours( 
    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
  
largest_countour = max(contours, key=cv2.contourArea)
print(":: Largest Contour Area:", cv2.contourArea(largest_countour))
# Loop through the contours and calculate the area of each object 
for cnt in contours: 
    area = cv2.contourArea(cnt) 
    if area < 1000:
        continue
  
    # Draw a bounding box around each 
    # object and display the area on the image 
    x, y, w, h = cv2.boundingRect(cnt) 
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) 
    cv2.putText(img, str(area), (x, y), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
# write the image to a file 
cv2.imwrite(f'sized_{fname}', img) 
