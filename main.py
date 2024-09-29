import cv2
import ascii_magic
import imgkit
import os

os.makedirs("images", exist_ok=True)
os.makedirs("ascii", exist_ok=True)
os.makedirs("html", exist_ok=True)

video_obj = cv2.VideoCapture("target")

count = 0
flag = True
while flag:
    flag, image = video_obj.read()
    if image is None:
        break
    cv2.imwrite(f"images/frame{count}.jpg", image)
    count += 1

for i in range(count):
    s = f"images/frame{i}.jpg"
    output = ascii_magic.from_image_file(
        s,
        columns=250,
        width_ratio=2,
        mode=ascii_magic.Modes.HTML
    )
    ascii_magic.to_html_file(f"html/frame{i}.html", output, additional_styles='background: #222;')
    print(f"Generated HTML: html/frame{i}.html")

path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe' 
config = imgkit.config(wkhtmltoimage=path)

for i in range(count):
    html_path = f'html/frame{i}.html'
    img_output = f'ascii/frame{i}.jpg'
    try:
        imgkit.from_file(html_path, img_output, config=config)
        if os.path.exists(img_output):
            print(f"Successfully created {img_output}")
        else:
            print(f"Error: Failed to create {img_output} from {html_path}")
    except Exception as e:
        print(f"Conversion failed for {html_path}: {e}")

frame_path = "ascii/frame0.jpg"
if not os.path.exists(frame_path):
    print(f"Error: {frame_path} not found.")
    exit()

frame = cv2.imread(frame_path)
if frame is None:
    print(f"Error: Could not load {frame_path}")
    exit()

ih, iw, il = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter("asciiVideo.mp4", fourcc, 23.98, (iw, ih))

for i in range(count):
    image_path = f"ascii/frame{i}.jpg"
    img = cv2.imread(image_path)
    if img is None:
        print(f"Warning: Could not load {image_path}")
        continue
    video.write(img)

cv2.destroyAllWindows()
video.release()
