from rembg import remove
from PIL import Image

print("===== Background Remover =====")

input_image = input("Enter input image name: ")
output_image = input("Enter output image name (with .png): ")

try:
    image = Image.open(input_image)
    output = remove(image)
    output.save(output_image)

    print(f"✅ Background removed successfully!")
    print(f"📁 Saved as: {output_image}")

except FileNotFoundError:
    print("Input image not found.")

except Exception as e:
    print(f"Error: {e}")