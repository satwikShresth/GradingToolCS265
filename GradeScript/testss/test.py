import subprocess
import os

# Run the C executable and redirect its output to a file
exe_path = './m'
output_file = 'output.txt'
with open(output_file, 'w') as f:
    subprocess.run([exe_path], stdout=f)

# Analyze the output file for memory leaks using valgrind
valgrind_cmd = ['valgrind', '--leak-check=full', '--error-exitcode=1', exe_path]
valgrind_output = subprocess.run(valgrind_cmd, stderr=subprocess.PIPE)

# If valgrind reports errors, print a warning message
if valgrind_output.returncode != 0:
    if "All heap blocks were freed -- no leaks are possible" in valgrind_output.stderr.decode('utf-8'):
        print("No memory Leak")
    else:
        print("Memory Leak")

# Delete the output file
os.remove(output_file)
