import os
import sys

try:
  import dataikuapi.dss.langchain.llm.DKULLM
except ImportError:
  print("oh no 1")

sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))

try:
  import dataikuapi.dss.langchain.llm.DKULLM
except ImportError:
  print("oh no 2")

sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join("..")))

import dataikuapi.dss.langchain.llm.DKULLM # does not fail anymore
