import pytest
import bike_sharing

from pathlib import Path

lib_path = str(Path(bike_sharing.__file__).parent)

ret = pytest.main(["-x", lib_path])
if ret !=0:
    raise Exception("Tests failed!")
