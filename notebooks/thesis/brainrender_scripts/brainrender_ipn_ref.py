import brainrender
from brainrender.scene import Scene
from vedo import Box

from commons import ipn_cams

brainrender.WHOLE_SCREEN = False
brainrender.SHADER_STYLE = "cartoon"
brainrender.ROOT_ALPHA = 0
brainrender.SHOW_AXES = False

struct_list = [("ipn", "gray", 0.5), ("fr_r", "#c54238", 0.5), ("fr_l", "#546dae", 0.5)]
# ("ipn_somas", "light_grey", 0.3),
# ("dors_ipn", "ultramarine_violet", 0.2),
# ("ventr_ipn", "blue_light", 0.2)]
# ("cell_core", "carrot", 0.8),
# ("ahb_ring", "sea_green_medium", 0.8),
# ("glomeruli", "turquoise", 0.8)]

sections_views = [
    (ipn_cams["sidecam_paramd"], [None]),  # [None, 103, 143, 183]),
    (ipn_cams["side_paramd"], [None]),
    (ipn_cams["front_paramd"], [None]),
    (ipn_cams["top_paramd"], [None]),
]
# ("frontal", [None]),
# ("sagittal", [None])]


for camera, planes in sections_views:
    for p in planes:
        scene = Scene(
            atlas_name="ipn_zfish_0.5um",
            root=False,
            inset=False,
            screenshots_folder=r"/Users/luigipetrucco/Desktop/projections_new",
        )
        scene.plotter.axes = (
            4 if camera["name"] == "oblique" else False
        )  # 13 if type(camera) is str else 4

        th = [scene.add_brain_region(r, color=c, alpha=a) for (r, c, a) in struct_list]
        print("th", th)
        scene.add_silhouette(*th, lw=1)

        if p is not None:
            plane_t = Box(
                pos=(65.5, p // 2, 58),
                length=100,
                width=0.001,
                height=100,
                c="white",
                alpha=0.0,
            ).triangulate()
            plane = Box(
                pos=(65.5, p // 2, 58),
                length=100,
                width=0.001,
                height=100,
                c="white",
                alpha=0.2,
            )
            scene.add(plane)
            sil = plane.silhouette().lw(3)
            sil._original_mesh = plane
            scene.add(sil)

            for m in th:
                contour = m.intersectWith(plane_t).lw(3)
                scene.add(contour)

        scene.render(
            camera=camera, zoom=camera["zoom"], interactive=False
        )  # , camera=camera if camera else None)
        view_name = camera["name"]  # camera if type(camera) is str else "oblique"
        plane_name = f"_plane{p}" if p else ""
        scene.screenshot(name=f"{view_name + plane_name}.png")
        # scene.show()
