from converter import *

print("1. Full Video")
print("2. First 10 Seconds")
print("3. Resize")
print("4. Low FPS")

choice = input("Choose: ")
video = input("Video: ")
output = input("Output: ")

if choice == "1":
    full(video, output)
elif choice == "2":
    first_ten_seconds(video, output)
elif choice == "3":
    resize(video, output)
elif choice == "4":
    low_fps(video, output)
else:
    print("Invalid option!")