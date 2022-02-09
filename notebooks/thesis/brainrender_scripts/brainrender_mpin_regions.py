# Requires the brainrender package:
import brainrender
from brainrender.scene import Scene

################################################################################
# Specify parameters ###########################################################

# Folder for the projections exporting. If set to None,
# viewer is opened in interactive mode and no screenshot is saved.
# If a folder is specified, it has to exist.
screenshots_folder = r"/Users/luigipetrucco/Desktop/projections_new"

# Brainrender configurator. SHADER_STYLE is the key parameter that change the appearence
# of the rendering (cartoonish or smooth or whathever).
# Options are "cartoon", "plastic", "ambient", "shiny", "glossy", "metallic"
brainrender.settings.SHADER_STYLE = "ambient"

# Other options:
brainrender.settings.WHOLE_SCREEN = False  # if True, press "q" to quit the viewer

brainrender.settings.ROOT_ALPHA = 0  # set the default root mesh to transparent
brainrender.settings.SHOW_AXES = False  # set to true if axes are wanted

# The atlas that we use:
atlas_name = "mpin_zfish_1um"

################################################################################
# Specify regions ##############################################################
# List of tuples. Each tuple is (region_name, color, alpha).
# Color could be a string (see https://vedo.embl.es/autodocs/_modules/vedo/colors.html)
# or a #FFFFFF string. Some suggestions:
# "#1b9e77"  green
# "#d95f02"  orange
# "#7570b3"  purple
# "#e7298a"  pink
# "#66a61e"  light gray
# "#e6ab02"  yellow
# "#a6761d"  brown
# See below for a list of structures.
# "brain" and "retina" are used for the outlining of brain and eyes.
struct_list = [
    ("brain", "#808080", 0.2),
    ("retina", "black", 0.2),
    ("interpeduncular nucleus", "#e7298a", 0.5),
    ("habenula", "#1b9e77", 0.5),
]

# Structures from BrainGlobe atlas:
# -- BRAIN STRUCTURES TREE --
# root (1)
# ├── brain (2)
# ├── mesencephalon (midbrain) (1007)
# │   ├── tectum & tori (954)
# │   │   ├── tectum (972)
# │   │   │   ├── periventricular layer (970)
# │   │   │   └── tectal neuropil (962)
# │   │   │       ├── boundary zone between SAC and periventricular layer (1000)
# │   │   │       ├── boundary zone between SFGS and SGC (926)
# │   │   │       ├── stratum album centrale (SAC) (1018)
# │   │   │       ├── stratum fibrosum et griseum superficiale (SFGS) (969)
# │   │   │       ├── stratum griseum centrale (SGC) (1024)
# │   │   │       ├── stratum marginale (SM) (995)
# │   │   │       └── stratum opticum (SO) (946)
# │   │   ├── torus longitudinalis (963)
# │   │   └── torus semicircularis (989)
# │   └── tegmentum (921)
# │       ├── lateral tegmentum (1008)
# │       └── medial tegmentum (entire) (999)
# │           ├── medial tegmentum (remaining) (1006)
# │           └── oculomotor nucleus (1015)
# ├── peripheral nervous system (976)
# │   ├── anterior lateral line ganglion (928)
# │   ├── glossopharyngeal ganglion (1009)
# │   ├── octaval ganglion (1002)
# │   ├── olfactory epithelium (920)
# │   ├── posterior lateral line ganglion (984)
# │   └── trigeminal ganglion (966)
# ├── prosencephalon (forebrain) (977)
# │   ├── eminentia thalami (933)
# │   │   ├── eminentia thalami (remaining) (978)
# │   │   └── ventral entopeduncular nucleus (975)
# │   ├── hypothalamus & preoptic area (979)
# │   │   ├── hypothalamus (973)
# │   │   │   ├── caudal hypothalamus (983)
# │   │   │   ├── intermediate hypothalamus (entire) (988)
# │   │   │   │   ├── diffuse nucleus of the inferior lobe (953)
# │   │   │   │   └── intermediate hypothalamus (remaining) (950)
# │   │   │   ├── pituitary (919)
# │   │   │   └── rostral hypothalamus (998)
# │   │   └── preoptic area (916)
# │   │       ├── retinal arborization field 1 (994)
# │   │       └── retinal arborization field 2 (948)
# │   ├── pretectum (1004)
# │   │   ├── nucleus of the medial longitudinal fascicle (pretectum, basal part) (1026)
# │   │   └── pretectum  alar part (960)
# │   │       ├── retinal arborization field 5 (949)
# │   │       ├── retinal arborization field 6 (992)
# │   │       ├── retinal arborization field 7 (1005)
# │   │       ├── retinal arborization field 8 (996)
# │   │       └── retinal arborization field 9 (1003)
# │   ├── prethalamus (ventral thalamus) (1013)
# │   │   ├── posterior tuberculum (basal part of prethalamus and thalamus) (982)
# │   │   └── ventral thalamus, alar part (915)
# │   │       └── retinal arborization field 3 (958)
# │   ├── retina (923)
# │   ├── telencephalon (1020)
# │   │   ├── olfactory bulb (1017)
# │   │   ├── pallium (dorsal telencephalon) (951)
# │   │   └── subpallium (ventral telencephalon) (918)
# │   └── thalamus (dorsal thalamus) (925)
# │       ├── dorsal thalamus proper (917)
# │       │   └── retinal arborization field 4 (957)
# │       ├── epiphysis (932)
# │       └── habenula (935)
# │           ├── dorsal habenula (939)
# │           └── ventral habenula (993)
# └── rhombencephalon (hindbrain) (1027)
#     ├── cerebellum (959)
#     ├── hindbrain rhombomeres (1011)
#     └── medulla oblongata (971)
#         ├── inferior medulla oblongata (980)
#         │   ├── inferior dorsal medulla oblongata (922)
#         │   │   ├── area postrema (987)
#         │   │   ├── inferior dorsal medulla oblongata stripe 1 (943)
#         │   │   ├── inferior dorsal medulla oblongata stripe 2&3 (965)
#         │   │   ├── inferior dorsal medulla oblongata stripe 4 (981)
#         │   │   ├── inferior dorsal medulla oblongata stripe 5 (985)
#         │   │   ├── vagal sensory lobe (1014)
#         │   │   └── vagus motor nucleus (947)
#         │   └── inferior ventral medulla oblongata (entire) (931)
#         │       ├── inferior olive (924)
#         │       ├── inferior raphe (936)
#         │       ├── inferior ventral medulla oblongata (remaining) (1019)
#         │       └── lateral reticular nucleus (1010)
#         ├── intermediate medulla oblongata (1021)
#         │   ├── intermediate dorsal medulla oblongata (986)
#         │   │   ├── intermediate dorsal medulla oblongata stripe 1 (991)
#         │   │   ├── intermediate dorsal medulla oblongata stripe 2&3 (956)
#         │   │   ├── intermediate dorsal medulla oblongata stripe 4 (929)
#         │   │   └── intermediate dorsal medulla oblongata stripe 5 (941)
#         │   └── intermediate ventral medulla oblongata (entire) (955)
#         │       ├── abducens motor nucleus (961)
#         │       ├── facial motor nucleus (944)
#         │       └── intermediate ventral medulla oblongata (remaining) (927)
#         └── superior medulla oblongata (940)
#             ├── superior dorsal medulla oblongata (937)
#             │   ├── medial octavolateralis nucleus (945)
#             │   ├── superior dorsal medulla oblongata stripe 1 (entire) (968)
#             │   │   ├── superior dorsal medulla oblongata stripe 1 (remaining) (974)
#             │   │   └── trochlear motor nucleus (934)
#             │   ├── superior dorsal medulla oblongata stripe 2&3 (1001)
#             │   ├── superior dorsal medulla oblongata stripe 4 (938)
#             │   └── superior dorsal medulla oblongata stripe 5 (930)
#             └── superior ventral medulla oblongata (entire) (1012)
#                 ├── anterior (dorsal) trigeminal motor nucleus (964)
#                 ├── interpeduncular nucleus (997)
#                 ├── locus coeruleus (1016)
#                 ├── nucleus isthmi (1025)
#                 │   ├── anterior cholinergic domain (1032)
#                 │   ├── gabaergic domain (1031)
#                 │   ├── glutamatergic domain (1029)
#                 │   └── posterior cholinergic domain (1030)
#                 ├── posterior (ventral) trigeminal motor nucleus (1022)
#                 ├── superior raphe (967)
#                 └── superior ventral medulla oblongata (remaining) (1023)


################################################################################
# Specify axis mode ############################################################
# Number from 0 to 13 specifying what kind of axes are shown.
# Short list below from https://vedo.embl.es/autodocs/content/vedo/plotter.html
#  0, no axes
#  1, draw three gray grid walls
#  2, show cartesian axes from (0,0,0)
#  3, show positive range of cartesian axes from (0,0,0)
#  4, show a triad at bottom left
#  5, show a cube at bottom left
#  6, mark the corners of the bounding box
#  7, draw a 3D ruler at each side of the cartesian axes
#  8, show the VTK CubeAxesActor object
#  9, show the bounding box outLine,
#  10, show three circles representing the maximum bounding box,
#  11, show a large grid on the x-y plane (use with zoom=8)
#  12, show polar axes.
#  13, draw a simple ruler at the bottom of the window
axis_mode = 0


################################################################################
# Specify cameras (advanced) ###################################################
# Camera settings for the various views. Those are used only if we are exporting
# screenshots. To move the orthogonal views, change the values for both "pos" and
# "focalPoint" to keep the camera orthogonal. Hopefully defaults should be good.
# Zoom changes the distance of the view. clippingRange can be ignored.

atlas_shape = (974, 359, 597)
cam_pos = [s / 2 for s in atlas_shape]

sidecam_paramd = dict(
    name="oblique",
    pos=(700.0083, -400.0731, 0.0218),
    zoom=0.4,
    viewup=(-0.42519, -0.8579, -0.2882),
    clippingRange=(0, 10000),
)

side_paramd = dict(
    name="side",
    pos=(cam_pos[0], cam_pos[1], 1500),
    focalPoint=(cam_pos[0], cam_pos[1], 0),
    zoom=1,
    viewup=(0, -1, 0),
    clippingRange=(0, 10000),
)

front_paramd = dict(
    name="front",
    pos=(1500, cam_pos[1], -cam_pos[2]),
    focalPoint=(0.0, cam_pos[1], -cam_pos[2]),
    zoom=1,
    viewup=(0, -1, 0),
    clippingRange=(0, 10000),
)

top_paramd = dict(
    name="top",
    pos=(cam_pos[0], -1500.0, -cam_pos[2]),
    focalPoint=(cam_pos[0], 0.0, -cam_pos[2]),
    zoom=1,
    viewup=(-1, 0, 0),
    clippingRange=(0, 10000),
)

# List of views that will be saved if in saving mode. There is the option to change
# The axis mode for each view, in case for example one wants to specify some axes only
# in some particular view. For example the oblique view has a triplet of arrows and the
# other views have none. By default all views use the axis_mode value:
sections_views = [
    (sidecam_paramd, axis_mode),
    (side_paramd, axis_mode),
    (front_paramd, axis_mode),
    (top_paramd, axis_mode),
]


def create_scene(atlas_name, struct_list, axis_mode, screenshots_folder=None):
    """Utility funct not to duplicate code, used in interacting and exporting mode."""
    scene = Scene(
        atlas_name=atlas_name,
        root=False,
        inset=False,
        screenshots_folder=screenshots_folder,
    )
    scene.plotter.axes = axis_mode
    th = [scene.add_brain_region(r, color=c, alpha=a) for (r, c, a) in struct_list]
    if brainrender.settings.SHADER_STYLE == "ambient":
        scene.add_silhouette(*th, lw=1)

    return scene


# If we go interactive mode:
if screenshots_folder is None:
    scene = create_scene(atlas_name, struct_list, axis_mode)
    scene.render(interactive=True, zoom=10)
else:
    # Otherwise, take snapshots:
    for camera, axis_mode in sections_views:
        scene = create_scene(
            atlas_name, struct_list, axis_mode, screenshots_folder=screenshots_folder
        )

        scene.render(camera=camera, zoom=camera["zoom"], interactive=False)

        scene.screenshot(name=f"{camera['name']}.png")
