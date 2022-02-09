################################################################################
# Specify cameras (advanced) ###################################################
# Camera settings for the various views. Those are used only if we are exporting
# screenshots. To move the orthogonal views, change the values for both "pos" and
# "focalPoint" to keep the camera orthogonal. Hopefully defaults should be good.
# Zoom changes the distance of the view. clippingRange can be ignored.

atlas_shape_mpin = (974, 359, 597)
cam_pos_mpin = [s / 2 for s in atlas_shape_mpin]

wholebrain_cams = dict(
    sidecam_paramd=dict(
        name="oblique",
        pos=(700.0083, -400.0731, 0.0218),
        zoom=0.4,
        viewup=(-0.42519, -0.8579, -0.2882),
        clippingRange=(0, 10000),
    ),
    side_paramd=dict(
        name="side",
        pos=(cam_pos_mpin[0], cam_pos_mpin[1], 1500),
        focalPoint=(cam_pos_mpin[0], cam_pos_mpin[1], 0),
        zoom=1,
        viewup=(0, -1, 0),
        clippingRange=(0, 10000),
    ),
    front_paramd=dict(
        name="front",
        pos=(1500, cam_pos_mpin[1], -cam_pos_mpin[2]),
        focalPoint=(0.0, cam_pos_mpin[1], -cam_pos_mpin[2]),
        zoom=1,
        viewup=(0, -1, 0),
        clippingRange=(0, 10000),
    ),
    top_paramd=dict(
        name="top",
        pos=(cam_pos_mpin[0], -1500.0, -cam_pos_mpin[2]),
        focalPoint=(cam_pos_mpin[0], 0.0, -cam_pos_mpin[2]),
        zoom=1,
        viewup=(-1, 0, 0),
        clippingRange=(0, 10000),
    ),
)

atlas_shape_ipn = 402, 350, 432
cam_pos_ipn = [s / 2 for s in atlas_shape_ipn]
clipping_range = (0, 10000)

ipn_cams = dict(
    sidecam_paramd=dict(
        name="oblique",
        pos=(253.0083, -81.0731, 217.0218),
        zoom=0.97,
        # focalPoint=(59.3447, 68.7675, 56.6614),
        viewup=(-0.42519, -0.8579, -0.2882),
        # distance=292.6997808562691,
        clippingRange=clipping_range,
    ),
    side_paramd=dict(
        name="side",
        pos=(cam_pos_ipn[0], cam_pos_ipn[1], 1500),
        focalPoint=(cam_pos_ipn[0], cam_pos_ipn[1], 0.0),
        zoom=4,
        viewup=(0, -1, 0),
        clippingRange=clipping_range,
    ),
    front_paramd=dict(
        name="front",
        pos=(1500, cam_pos_ipn[1], -cam_pos_ipn[2]),
        focalPoint=(0.0, cam_pos_ipn[1], -cam_pos_ipn[2]),
        zoom=4,
        viewup=(0, -1, 0),
        clippingRange=clipping_range,
    ),
    top_paramd=dict(
        name="top",
        pos=(cam_pos_ipn[0], -1500.0, -cam_pos_ipn[2]),
        focalPoint=(cam_pos_ipn[0], 0.0, -cam_pos_ipn[2]),
        zoom=4,
        viewup=(-1, 0, 0),
        clippingRange=clipping_range,
    ),
)
