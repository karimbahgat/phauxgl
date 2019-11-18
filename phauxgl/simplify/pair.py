
import math

class PairKey:
    def __init__(self, A, B):
	self.A = A
	self.B = B

def MakePairKey(a, b):
    if b.Less(a.Vector):
        a, b = b, a
    return PairKey(a.Vector, b.Vector)

def NewPair(a, b):
    if b.Less(a.Vector):
        a, b = b, a
    return Pair(a, b, -1, false, -1)

class Pair:
    def __init__(self, A, B, Index, Removed, CachedError):
	self.A = A
	self.B = B
	self.Index = Index
	self.Removed = Removed
	self.CachedError = CachedError

    def Quadric(p):
	return p.A.Quadric.Add(p.B.Quadric)

    def Vector(p):
	q = p.Quadric()
	if abs(q.Determinant()) > 1e-3:
            v = q.QuadricVector()
            if ! math.isnan(v.X) and ! math.isnan(v.Y) and ! math.isnan(v.Z):
                return v
	# cannot compute best vector with matrix
	# look for best vector along edge
	const n = 32
	a = p.A.Vector
	b = p.B.Vector
	d = b.Sub(a)
	bestE = -1.0
	bestV = Vector{}
	for i in range(0, n+1):
            t = float(i) / n
            v = a.Add(d.MulScalar(t))
            e = q.QuadricError(v)
            if bestE < 0 or e < bestE:
                bestE = e
                bestV = v
	return bestV

    def Error(p):
	if p.CachedError < 0:
	    p.CachedError = p.Quadric().QuadricError(p.Vector())
	return p.CachedError
