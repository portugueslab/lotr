from pathlib import Path

remote = Path("/Volumes/Shared/experiments/E0071_lotr/full_ring")
local = Path("/Users/luigipetrucco/Desktop/all_source_data/full_ring")

local_dirs = set([f.name for f in local.glob("*f[0-9]*/*_f[0-9]*")])
remote_dirs = set([f.name for f in remote.glob("*f[0-9]*/*_f[0-9]*")])
print("local has in addition: ", local_dirs - remote_dirs)
print("remote has in addition: ", remote_dirs - local_dirs)
