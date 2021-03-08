def getVectorAngle(v1,v2):
    value = dot(v1, v2)
    return acos(value / (mag(v1) * mag(v2)))

def mag(vec):
    (x, y, z) = vec
    return (x**2+y**2+z**2)**0.5