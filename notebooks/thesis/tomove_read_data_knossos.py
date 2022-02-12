from knossos_utils import knossosdataset
import numpy as np
import flammkuchen as fl
from pathlib import Path

config_path = Path("/Users/luigipetrucco/Google Drive/data/em_stack/knossos.conf")
dir_save_path = Path(r"/Users/luigipetrucco/Desktop/em_stack_highres")

# Size of the columns:
size_x = 1000
size_z = 7500 # 4000
size_y = 1000

# offset of the columns:
start_x = 17000 # 20000
start_z = 17000 # 6000
start_y = 5800 # 20000

dwn = 1 # downsampling factor
mag = 4   # magnification

# Size of the columns:
size_x = size_x / mag
size_z = size_z / mag # 4000
size_y = size_y / mag

# offset of the columns:
start_x = start_x / mag # 20000
start_z = start_z / mag # 6000
start_y = start_y / mag # 20000

dir_save_path.mkdir(exist_ok=True)  # make dest directory if missing

kd = knossosdataset.KnossosDataset()
kd.initialize_from_conf(str(config_path))  # initialize dataset

print(kd.boundary)
print("loading data...(cube to mat )")
for ix in range(11):
    offx = start_x + ix * size_x
    for iy in range(6):
        offy = start_y + iy * size_y
        print(offx, offy)
        raw = kd.from_raw_cubes_to_matrix(size=(size_x, size_z, size_y),
                          offset=(offx, start_z, offy),
                          mag=mag,
                          datatype=np.uint8)

        print(raw.shape)
        fl.save(dir_save_path / f"em_data{ix}_{iy}.h5", dict(stack_3D=raw[::dwn,::dwn,::dwn]))



# lines in mergelist tools setup at line 15:
#        extra_compile_args=['-stdlib=libc++'],
 #       extra_link_args=['-stdlib=libc++'])

