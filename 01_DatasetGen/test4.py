import gtsam

br_i1 = gtsam.BearingRange3D.Measure(gtsam.Pose3(gtsam.Rot3.RzRyRx(2.5, 0.5, 0.2), gtsam.Point3(1,2,3)), gtsam.Point3(2, 2, 0))
print(br_i1.range())
print(br_i1.bearing().point3())

Twb = gtsam.Pose3(gtsam.Rot3.RzRyRx(2.5, 0.5, 0.2), gtsam.Point3(1,2,3))
pt_body = br_i1.range() * br_i1.bearing().point3()
pt_world = Twb.transformFrom(pt_body)

print(pt_world)