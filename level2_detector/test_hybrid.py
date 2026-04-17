from hybrid_detector import detect_and_classify

image_path = "test.jpg"   # put any test image here

result = detect_and_classify(image_path)

print("\n=== DETECTION RESULT ===")
print("Dry count:", result["dry_count"])
print("Wet count:", result["wet_count"])
print("Annotated image saved at:", result["result_image"])

print("\nObjects:")
for obj in result["detections"]:
    print(obj)