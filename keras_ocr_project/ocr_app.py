# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
# from msrest.authentication import CognitiveServicesCredentials
# import time

# # Replace with your Azure endpoint and API key
# subscription_key = "G0IEmnshA6IQxEWeqJhAQEQJ3QbMRb7Of5MiGCmiKS6fP4gV5hZiJQQJ99BBACqBBLyXJ3w3AAAFACOGfuao"
# endpoint = "https://agileocr.cognitiveservices.azure.com/"

# # Authenticate the client
# computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# # Path to the image file
# image_path = "prescription (2).png"

# # Open the image file
# with open(image_path, "rb") as image_file:
#     # Call the API to read text from the image
#     recognize_handwriting_results = computervision_client.read_in_stream(image_file, raw=True)

# # Get the operation location (URL with the operation ID)
# operation_location = recognize_handwriting_results.headers["Operation-Location"]
# operation_id = operation_location.split("/")[-1]

# # Wait for the operation to complete
# while True:
#     result = computervision_client.get_read_result(operation_id)
#     if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
#         break
#     time.sleep(1)

# # Extract and print the recognized text
# if result.status == OperationStatusCodes.succeeded:
#     for text_result in result.analyze_result.read_results:
#         for line in text_result.lines:
#             print(line.text)



# Azure Computer Vision
# Azure Computer Vision
# Azure Computer Vision
# Azure Computer Vision
# Azure Computer Vision


# import os
# import keras_ocr
# import cv2
# import matplotlib.pyplot as plt

# # Fix potential GPU issues
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU if not available

# # Load the pre-trained Keras-OCR pipeline
# print("Loading Keras-OCR pipeline...")
# pipeline = keras_ocr.pipeline.Pipeline()


# def recognize_text(image_path):
#     """
#     Recognizes text from an image using Keras-OCR.
    
#     Parameters:
#     image_path (str): Path to the image file.
    
#     Returns:
#     None (Displays image with detected text)
#     """
#     try:
#         # Read the image
#         image = keras_ocr.tools.read(image_path)
        
#         # Run the OCR pipeline
#         predictions = pipeline.recognize([image])
        
#         # Draw detected text on the image
#         keras_ocr.tools.drawAnnotations(image=image, predictions=predictions[0])
        
#         # Display the image with detected text
#         plt.imshow(image)
#         plt.axis("off")  # Hide axes
#         plt.show()
        
#         # Print extracted text
#         print("\nDetected Text:")
#         for word, box in predictions[0]:
#             print(f"- {word}")

#     except Exception as e:
#         print(f"Error in OCR processing: {e}")


# if __name__ == "__main__":
#     # Provide the path to the input image
#     img_path = "ss.png"  # Change this to your image filename
#     if os.path.exists(img_path):
#         recognize_text(img_path)
#     else:
#         print(f"Error: Image file '{img_path}' not found. Please provide a valid image.")

# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64
# azure base 64


import io
import base64
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

# Azure credentials
endpoint = "https://agileocr.cognitiveservices.azure.com/"
subscription_key = "G0IEmnshA6IQxEWeqJhAQEQJ3QbMRb7Of5MiGCmiKS6fP4gV5hZiJQQJ99BBACqBBLyXJ3w3AAAFACOGfuao"

# Initialize Computer Vision Client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Base64 image string (replace with your actual base64 string)
base64_string = "iVBORw0KGgo..."  # Truncated for brevity

# Decode base64 string to bytes
image_bytes = base64.b64decode(base64_string)

image_stream = io.BytesIO(image_bytes)

# Call the API to read text from the image

recognize_handwriting_results = computervision_client.read_in_stream(image_stream, raw=True)

# Get the operation location (URL with the operation ID)
operation_location = recognize_handwriting_results.headers["Operation-Location"]
operation_id = operation_location.split("/")[-1]

# Wait for the operation to complete
while True:
    result = computervision_client.get_read_result(operation_id)
    if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
        break
    time.sleep(1)


print("hello")

# Extract and print the recognized text
if result.status == OperationStatusCodes.succeeded:
    print(result.status)
    for text_result in result.analyze_result.read_results:
        print(text_result)
        for line in text_result.lines:
            print("hello3")
            print(line.text)




# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# import keras_ocr
# import base64
# import io
# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

# # Function to decode Base64 to PIL image
# def decode_base64_to_image(base64_string):
#     image_data = base64.b64decode(base64_string)
#     image = Image.open(io.BytesIO(image_data))
#     return image

# # Sample Base64 string (Replace this with your actual Base64 string)
# base64_string = "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"  # Truncated example


# # Decode the image
# decoded_image = decode_base64_to_image(base64_string)
# decoded_image.show()  # Display the original image to verify it's loaded correctly

# # Convert PIL Image to NumPy Array
# image_np = np.array(decoded_image.convert("RGB"), dtype=np.uint8)

# # Initialize keras-ocr pipeline
# pipeline = keras_ocr.pipeline.Pipeline()

# # Perform OCR
# predictions = pipeline.recognize([image_np])

# # Verify Predictions
# print("Detected Text:")
# for text, box in predictions[0]:
#     print(f"{text}: {box}")

# # Annotate Image
# annotated_image = keras_ocr.tools.drawAnnotations(image=image_np, predictions=predictions[0])

# # Display Image with Annotations
# plt.figure(figsize=(10, 10))
# plt.imshow(annotated_image)
# plt.axis("off")
# plt.show()



# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64
# keras base64