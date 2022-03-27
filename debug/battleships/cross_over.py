import copy
import numpy as np

class method_cross_over(object):
    def __init__(self,candidate,N):
        self.candidate = candidate
        self.N = N
    
    def point(self,b):
        count = 0
        for i in range(0,self.N - 1):
            for j in range(i + 1,self.N):
                if b[i] + j == b[j]:
                    count += 1
                if b[i] - j == b[j]:
                    count += 1
                if b[i] == b[j]:
                    count += 1
        return (self.N * (self.N - 1))/2 - count
    
    def half_gen(self,a,b):
        a_head = np.array(copy.deepcopy(a))
        b_head = np.array(copy.deepcopy(b))
        
        a_tail = np.array(copy.deepcopy(a))
        b_tail = np.array(copy.deepcopy(b))
      
        swap_ele = self.N//2 
        #-------------------------------------
        a_head[:swap_ele],b_head[:swap_ele] = b_head[:swap_ele],a_head[:swap_ele]
        a_tail[swap_ele:],b_tail[swap_ele:] = b_tail[swap_ele:],a_tail[swap_ele:]
        #-------------------------------------
        res = np.zeros(4)
        
        res[0] = self.point(a_head)
        res[1] = self.point(b_head)
        res[2] = self.point(a_tail)
        res[3] = self.point(b_tail)
        
        res = np.argsort(res)[::-1][0]
        
        if res == 0: self.candidate.append(a_head)
        elif res == 1: self.candidate.append(b_head)
        elif res == 2: self.candidate.append(a_tail)
        else: self.candidate.append(b_tail)
        
        return None
        
    def multipoint_cross_over(self,a,b):
        a_can = copy.deepcopy(a)
        b_can = copy.deepcopy(b)
        
        count = 0
        
        while np.array_equal(np.array(a_can),np.array(a)):
            begin = np.random.randint(0,self.N//2)
            end = np.random.randint(self.N//2,self.N + 1)
            a_can[begin : end],b_can[begin : end] = b_can[begin : end],a_can[begin : end]
            count += 1
            if count == 10:
                return None
        
        res_a = self.point(a_can)
        res_b = self.point(b_can)
        
        if res_a > res_b: self.candidate.append(np.array(a_can))
        else: self.candidate.append(np.array(b_can))
        
        return None
    
    def uniform_crossover(self,a,b):
        a_can = copy.deepcopy(a)
        b_can = copy.deepcopy(b)
        flip = np.binary_repr(np.random.randint(1,pow(2,self.N)),self.N)
        for i in range(self.N):
            if flip[i] == '1':
                a_can[i],b_can[i] = b_can[i],a_can[i]
        res_a = self.point(np.array(a_can))
        res_b = self.point(np.array(b_can))
        
        if res_a > res_b: self.candidate.append(np.array(a_can))
        else: self.candidate.append(np.array(b_can))
        
        return None
    
    def davidOrderCrossover(self,a,b):
        if np.array_equal(np.array(a),np.array(b)):
            return None
        b_can = copy.deepcopy(list(b))
        while np.array_equal(np.array(b),np.array(b_can)):
            begin = np.random.randint(0,self.N//2)
            end = np.random.randint(self.N//2,self.N + 1)
            
            temp_begin = copy.deepcopy(b_can[0 : begin])
            temp_end = copy.deepcopy(b_can[end : ])
            temp_middle = copy.deepcopy(list(a[begin: end]))
            
            b_can = []
            
            if len(temp_begin) > 0:
                b_can = temp_begin
            if len(temp_middle) > 0:
                b_can += temp_middle
            if len(temp_end) > 0:
                b_can += temp_end
            # b_can = b_can[0 : self.N]
            
        self.candidate.append(np.array(b_can))
        return None
    
    def get_candidate(self):
        return self.candidate