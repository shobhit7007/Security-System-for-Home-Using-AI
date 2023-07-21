'''
# importing the required modules
import cv2
import numpy as np

# capturing from the first camera attached
cap = cv2.VideoCapture(0)

# will continue to capture until 'q' key is pressed
while True:
	ret, frame = cap.read()

	# Capturing in grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	cv2.imshow('frame', frame)
	cv2.imshow('gray', gray)

	# Program will terminate when 'q' key is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#peepee = cap[]
# Releasing all the resources
cap.release()
#peepee.release()
cv2.destroyAllWindows()
# Loading modules
'''
import cv2
import numpy as np     # Numpy module will be used for horizontal stacking of two frames

video=cv2.VideoCapture(0)
a=0
while True:
    a=a+1
    check, frame= video.read()

    # Converting the input frame to grayscale
    gray=cv2.cvtColor(frame, cv2.COLOR_RGB2HLS_FULL)   

    # Fliping the image as said in question
    gray_flip = cv2.flip(frame,1)

    # Combining the two different image frames in one window
    combined_window = np.hstack([frame,gray_flip])

    # Displaying the single window
    cv2.imshow("Combined videos ",gray_flip)
    key=cv2.waitKey(1)

    if key==ord('q'):
        break
print(a)

video.release()
cv2.destroyAllWindows()
