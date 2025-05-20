import cv2
import numpy as np

def analyze_skin_tone(image):
    # Convert to YCrCb color space
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    # Define skin color range
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    
    # Create a mask
    mask = cv2.inRange(ycrcb, lower, upper)
    
    # Apply the mask to the original image
    skin = cv2.bitwise_and(image, image, mask=mask)
    
    # Calculate average color of skin pixels
    skin_tone = cv2.mean(skin, mask=mask)[:3]
    
    # Classify skin tone (this is a simple classification, can be improved)
    if skin_tone[2] > 150:
        return "light"
    elif skin_tone[2] > 100:
        return "medium"
    else:
        return "dark"

def suggest_colors(skin_tone):
    color_suggestions = {
        "light": ["Navy", "Burgundy", "Forest Green", "Plum", "Teal"],
        "medium": ["Coral", "Olive", "Turquoise", "Magenta", "Gold"],
        "dark": ["Ivory", "Peach", "Lavender", "Sky Blue", "Emerald"]
    }
    return color_suggestions.get(skin_tone, ["No specific suggestions"])

def change_skin_tone(image, new_tone):
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into L, A, and B channels
    l, a, b = cv2.split(lab)
    
    # Apply contrast stretching to L channel
    l_stretched = cv2.normalize(l, None, 0, 255, cv2.NORM_MINMAX)
    
    # Modify the A and B channels based on the new tone
    if new_tone == "light":
        a = cv2.add(a, 10)
        b = cv2.add(b, 10)
    elif new_tone == "dark":
        a = cv2.subtract(a, 10)
        b = cv2.subtract(b, 10)
    
    # Merge the channels back
    lab_modified = cv2.merge((l_stretched, a, b))
    
    # Convert back to BGR color space
    result = cv2.cvtColor(lab_modified, cv2.COLOR_LAB2BGR)
    
    return result