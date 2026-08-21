import hashlib

challenge = "485087211aa8a4e9"

i = 0
while True:
    x = str(i)
    if hashlib.sha256((challenge + x).encode()).hexdigest().startswith("00000"):
        print("solution:", x)
        break
    i += 1

