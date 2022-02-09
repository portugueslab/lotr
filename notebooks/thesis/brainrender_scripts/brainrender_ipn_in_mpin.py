# Requires the brainrender package:
import brainrender
from brainrender.scene import Scene
from brainrender.atlas import Atlas
from cameras import wholebrain_cams

# The supplementary IPN atlas that we use:
atlas_ipn = Atlas("ipn_zfish_0.5um")

################################################################################
# Specify parameters ###########################################################

# Folder for the projections exporting. If set to None,
# viewer is opened in interactive mode and no screenshot is saved.
# If a folder is specified, it has to exist.
screenshots_folder = None  # r"/Users/luigipetrucco/Desktop/projections_new"

# Brainrender configurator. SHADER_STYLE is the key parameter that change the appearence
# of the rendering (cartoonish or smooth or whathever).
# Options are "cartoon", "plastic", "ambient", "shiny", "glossy", "metallic"
brainrender.settings.SHADER_STYLE = "plastic"

# Other options:
brainrender.settings.WHOLE_SCREEN = False  # if True, press "q" to quit the viewer

brainrender.settings.ROOT_ALPHA = 0.2  # set the default root mesh to transparent
brainrender.settings.SHOW_AXES = False  # set to true if axes are wanted

################################################################################
# Specify regions ##############################################################
# List of tuples. Each tuple is (region_name, color, alpha).
# Color could be a string (see https://vedo.embl.es/autodocs/_modules/vedo/colors.html)
# or a #FFFFFF string. Some suggestions:
# "#1b9e77"  green
# "#d95f02"  orange
# "#7570b3"  purple
# "#e7298a"  pink
# "#66a61e"  light green
# "#e6ab02"  yellow
# "#a6761d"  brown

# Structures from the MPIN atlas:
# "brain" and "retina" are used for the outlining of brain and eyes.
struct_list_mpin = [
    ("brain", "#808080", 0.2),
    ("retina", "black", 0.2),
    ("interpeduncular nucleus", "#e7298a", 0.5),
    ("habenula", "#1b9e77", 0.5),
]

# Structures from the IPN atlas:
struct_list_ipn = [
    ("ipn", "salmon", 0.2),
    ("ahb_ring", "#66a61e", 0.2),
]


axis_mode = 0


# List of views that will be saved if in saving mode. There is the option to change
# The axis mode for each view, in case for example one wants to specify some axes only
# in some particular view. For example the oblique view has a triplet of arrows and the
# other views have none. By default all views use the axis_mode value:
sections_views = [
    (wholebrain_cams["sidecam_paramd"], axis_mode),
    (wholebrain_cams["side_paramd"], axis_mode),
    (wholebrain_cams["front_paramd"], axis_mode),
    (wholebrain_cams["top_paramd"], axis_mode),
]


def create_scene(
    struct_list_mpin, struct_list_ipn, atlas_ipn, axis_mode, screenshots_folder=None
):
    """Utility funct not to duplicate code, used in interacting and exporting mode."""
    scene = Scene(
        atlas_name="mpin_zfish_1um",
        root=False,
        inset=False,
        screenshots_folder=screenshots_folder,
    )

    # plot MPIN regions:
    scene.plotter.axes = axis_mode
    actors_mpin = [
        scene.add_brain_region(r, color=c, alpha=a) for (r, c, a) in struct_list_mpin
    ]
    print(actors_mpin)
    to_add_ipn = [
        atlas_ipn.get_region(r, alpha=a, color=c) for (r, c, a) in struct_list_ipn
    ]
    print(to_add_ipn)
    actors_ipn = scene.add(*to_add_ipn)

    mtx = [[1, 0, 0, 410], [0, 1, 0, 90], [0, 0, -1, -200], [0, 0, 0, 1]]
    [actor._mesh.applyTransform(mtx) for actor in actors_ipn]

    if brainrender.settings.SHADER_STYLE == "ambient":
        scene.add_silhouette(*(actors_mpin + actors_ipn), lw=1)

    return scene


# If we go interactive mode:
if screenshots_folder is None:
    scene = create_scene(struct_list_mpin, struct_list_ipn, atlas_ipn, axis_mode)
    scene.render(interactive=True, zoom=10)
else:
    # Otherwise, take snapshots:
    for camera, axis_mode in sections_views:
        scene = create_scene(
            struct_list_mpin,
            struct_list_ipn,
            atlas_ipn,
            axis_mode,
            screenshots_folder=screenshots_folder,
        )

        scene.render(camera=camera, zoom=camera["zoom"], interactive=False)

        scene.screenshot(name=f"{camera['name']}.png")
