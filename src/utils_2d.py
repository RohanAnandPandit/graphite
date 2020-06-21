def getVectorAngle(v1,v2):
    value = dot(v1, v2)
    return acos(value / (mag(v1) * mag(v2)))
