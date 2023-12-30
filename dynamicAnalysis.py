import streamlit as st
from PIL import Image
import easyocr as ocr
import pygetwindow as gw
import numpy as np
import os
import keyboard
import pyautogui
import time
import string
from collections import Counter
import matplotlib.pyplot as plt

st.title("Easy OCR - Extract text from Images")

# Specify the directory where screenshots are saved
screenshot_directory = r'D:\projects\chat analysis\prooj'

# Variable to keep track of the screenshot capture state
capture_screenshots = False
screenshot_count = 0  # To keep track of the number of screenshots taken

# Maximum number of screenshots to capture before pausing
max_screenshots = 6

# Title of the WhatsApp Web browser window in Google Chrome
whatsapp_web_title = "WhatsApp - Google Chrome"


# Load the OCR model
@st.cache(allow_output_mutation=True)
def load_ocr_model():
    reader = ocr.Reader(['en'], model_storage_directory='.')
    return reader

reader = load_ocr_model()

# Function to start screenshot capture when WhatsApp Web is active
def start_screenshot_capture():
    global capture_screenshots, screenshot_count
    if not capture_screenshots:
        capture_screenshots = True
        print("Screenshot capture started.")
        screenshot_count = 0  # Reset the screenshot count
        while capture_screenshots:
            if screenshot_count >= max_screenshots:
                stop_screenshot_capture()
            active_window = gw.getActiveWindow()
            if active_window and active_window.title == whatsapp_web_title:
                # Get the WhatsApp Web window size and position
                left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
                # Capture screenshot with the size of WhatsApp Web window
                screenshot = pyautogui.screenshot(region=(left, top, width, height))
                screenshot_name = f"screenshot_{screenshot_count}.png"
                screenshot_path = os.path.join(screenshot_directory, screenshot_name)
                screenshot.save(screenshot_path)
                print(f"Saved {screenshot_name}")
                screenshot_count += 1
                time.sleep(2)  # Wait 2 seconds before capturing the next screenshot
            time.sleep(1)   # Check every second if WhatsApp Web is active

# Function to stop screenshot capture
def stop_screenshot_capture():
    global capture_screenshots
    if capture_screenshots:
        capture_screenshots = False
        print("Screenshot capture stopped.")

# Function to capture and save a screenshot with a unique name
def capture_and_save_screenshots():
    global screenshot_count
    if capture_screenshots:
        screenshot = pyautogui.screenshot()
        screenshot_name = f"screenshot_{screenshot_count}.png"
        screenshot_path = os.path.join(screenshot_directory, screenshot_name)
        screenshot.save(screenshot_path)
        print(f"Saved {screenshot_name}")
        screenshot_count += 1
        time.sleep(2)  # Wait 2 seconds before capturing the next screenshot

# List to store OCR results
ocr_results = []

# Add separate buttons for starting and stopping screenshot capture
start_button = st.button("Start Screenshot Capture (Press 'S')")
stop_button = st.button("Stop Screenshot Capture (Press 'X')")

if start_button:
    start_screenshot_capture()

if stop_button:
    stop_screenshot_capture()

# Get a list of image files in the specified directory
image_files = [f for f in os.listdir(screenshot_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if image_files:
    for image_file in image_files:
        image_path = os.path.join(screenshot_directory, image_file)
        input_image = Image.open(image_path)

        st.image(input_image)  # Display the image for user understanding

        with st.spinner("AI at work!!"):
            result = reader.readtext(np.array(input_image))
            result_text = []  # Empty list for storing results

            for text in result:
                result_text.append(text[1])
            st.write(result_text)
            ocr_results.extend(result_text)  # Add results to the list

        st.success(f"Here are the extracted texts from the image: {image_file}")

# Create a text file and write OCR results
if ocr_results:
    text_file_path = os.path.join(screenshot_directory, "text.txt")
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write("\n".join(ocr_results))
    st.write("OCR results have been saved to 'text.txt'")

else:
    st.write("No image files found in the specified directory.")


st.title("Emotion Analysis from Text")
if 'text.txt' in os.listdir(screenshot_directory):
    with open(os.path.join(screenshot_directory, 'text.txt'), 'r', encoding='utf-8') as text_file:
        text = text_file.read()
else:
    uploaded_file = st.file_uploader("Upload a text file")
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
    else:
        st.write("Please upload a text file for emotion analysis.")
        st.stop()


lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('','',string.punctuation))


tokenized_words = cleaned_text.split()


stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

# Removing stop words from the tokenized words list
final_words = []
for word in tokenized_words:
    if word not in stop_words:
        final_words.append(word)

emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
        word, emotion = clear_line.split(':')

        if word in final_words:
            emotion_list.append(emotion)

print(emotion_list)
w = Counter(emotion_list)
print(w)

# Plotting the emotions on the graph

fig, ax1 = plt.subplots()
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()
plt.xlabel('Emotions')
plt.ylabel('Frequency')
plt.title('Emotion Analysis')
    
    # Display the plot using Streamlit
st.pyplot(fig)