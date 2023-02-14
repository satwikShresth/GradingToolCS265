import subprocess
import errno
import signal
import sys,os


def run_c_executable(input_str):
    prop = subprocess.getstatusoutput(f"./m")
    return prop[1]

input_str = "input_to_stdin"
fruits = [
                "apple",
                "Orange",
                "banana",
                "Strawberry",
                "Grape",
                "Blueberry",
                "Raspberry",
                "Pineapple",
                "Mango",
                "Watermelon",
                "Cantaloupe",
                "Peach",
                "Cherry",
                "Kiwi",
                "Apricot",
                "Lemon",
                "Lime",
                "Grapefruit",
                "Pomegranate",
                "Blackberry"
            ]
output = run_c_executable(input_str)
fileContents = [line for line in output.splitlines() if line.strip()]
for i in fruits:
    if i in output:
        print(f" {i} is in output")
print(fileContents)
