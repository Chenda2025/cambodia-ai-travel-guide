import base64

with open("static/images/hero.jpg", "rb") as img_file:
    base64_string = base64.b64encode(img_file.read()).decode()

print(base64_string)