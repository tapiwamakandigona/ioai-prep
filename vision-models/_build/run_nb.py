import sys, time
import nbformat
from nbclient import NotebookClient
path = sys.argv[1]
nb = nbformat.read(path, as_version=4)
t0 = time.time()
client = NotebookClient(nb, timeout=900, kernel_name="python3", resources={"metadata": {"path": "/work/projects/ioai-prep/vision-models/notebooks"}})
client.execute()
nbformat.write(nb, path)
print(f"EXECUTED OK: {path} in {time.time()-t0:.0f}s")
