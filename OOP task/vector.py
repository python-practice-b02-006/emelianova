import numpy as np

class MyVector():
    
    def __init__(self, a=0, b=0, c=0):
        self.x = a
        self.y = b
        self.z = c
        
    def __add__(self, inst):
        return MyVector(self.x + inst.x, self.y + inst.y, self.z + inst.z)
    
    def __matmul__(self, inst):
        a = self.y * inst.z - self.z * inst.y 
        b = self.z * inst.x - self.x * inst.z 
        c = self.x * inst.y - self.y * inst.x 
        return MyVector(a, b, c)
    
    def __mul__(self, inst):
        if type(inst) == int:
            return MyVector(self.x*inst, self.y*inst, self.z*inst)
        if isinstance(inst, MyVector):
            return self.x * inst.x + self.y * inst.y + self.z * inst.z
        
    def __rmul__(self, inst):
        if type(inst) == int:
            return MyVector(self.x*inst, self.y*inst, self.z*inst)
    
    def __str__(self):
        return str('('+str(self.x)+','+str(self.y)+','+str(self.z) + ')')

    def module(self):
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __sub__(self, inst):
        return MyVector(self.x - inst.x, self.y - inst.y, self.z - inst.z)
    
    def __neg__(self):
        return self*(-1)
    
    
inst1 = MyVector(1, 8, -1)
inst2 = MyVector(9, -5, 2)
inst3 = MyVector(7, 4, 5)

print('a =', inst1, ' b =', inst2, ' c =', inst3)

print('[a, [b, c]] =',  inst1@(inst2@inst3))
print('b*(a, c) - c*(a, b) =', inst2*(inst1*inst3) - inst3*(inst1*inst2))
print('module of [a, [b, c]] = ', (inst1@(inst2@inst3)).module())
