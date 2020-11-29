from sys import platform
import os
if platform == "linux" or platform == "linux2":
    print("You`re using Linux")
elif platform == "darwin":
    print("You`re using MacOS")
elif platform == "win32":
    print("You`re using Windows")
