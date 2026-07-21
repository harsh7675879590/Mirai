import imageio
from PIL import Image, ImageSequence

input_file = "C:/Users/harsh/.gemini/antigravity-ide/brain/6d618d79-7630-4f99-a385-f4890401f456/visual_novel_gameplay_1784632752769.webp"
output_file = "C:/Users/harsh/.gemini/antigravity-ide/brain/6d618d79-7630-4f99-a385-f4890401f456/visual_novel_gameplay_fixed.mp4"

print("Reading webp...")
img = Image.open(input_file)

writer = imageio.get_writer(output_file, fps=10) # Using a default 10fps for screen capture

import numpy as np

count = 0
for frame in ImageSequence.Iterator(img):
    # Convert frame to RGB and then to numpy array
    frame = frame.convert("RGB")
    frame_array = np.array(frame)
    writer.append_data(frame_array)
    count += 1

writer.close()
print(f"Done! Extracted {count} frames to MP4.")
