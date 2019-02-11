import f90nml
import sys

file_path = sys.argv[1]
print(file_path)
prefix = sys.argv[2]
print(prefix)

inp = f90nml.read(file_path)

ung=inp['ungrib']

ung['prefix'] = prefix

f90nml.write(inp,file_path,force=True)
