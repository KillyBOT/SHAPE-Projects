# -*- coding: utf-8 -*-

from SortingAlgorithms import MergeSort

def GCF(a, b):
    if a < b:
        b,a = a,b
    if a % b == 0:
        return b
    return GCF(b, a % b)
        
def LCM(a,b):
    gcf = GCF(a,b)
    return (a*b)/gcf

class Fraction(object):
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        
        if GCF(self.numerator, self.denominator) != 1:
            tempNumerator = self.numerator
            tempDenominator = self.denominator
            self.numerator /= GCF(tempNumerator, tempDenominator)
            self.denominator /= GCF(tempNumerator, tempDenominator)

    def __str__(self):
        return str("%d/%d" % (self.numerator, self.denominator))
        
    def __repr__(self):
        return str("%d/%d" % (self.numerator, self.denominator))
        
    def __add__(self, other):
        #print(LCM(self.denominator, other.denominator))
        newDenominator = LCM(self.denominator, other.denominator)
        newNumerator = self.numerator*(newDenominator/self.denominator) + other.numerator*(newDenominator/other.denominator)
        return Fraction(newNumerator, newDenominator)
        
    def __gt__(self, other):
        newDenominator = LCM(self.denominator, other.denominator)
        if(self.numerator*(newDenominator/self.denominator) > other.numerator*(newDenominator/other.denominator)):
            return True
        else:
            return False
            
    def __eq__(self, other):
        newDenominator = LCM(self.denominator, other.denominator)
        if(self.numerator*(newDenominator/self.denominator) == other.numerator*(newDenominator/other.denominator)):
            return True
        else:
            return False
            
    def __lt__(self, other):
        newDenominator = LCM(self.denominator, other.denominator)
        if(self.numerator*(newDenominator/self.denominator) < other.numerator*(newDenominator/other.denominator)):
            return True
        else:
            return False
            
    def __ge__(self, other):
        newDenominator = LCM(self.denominator, other.denominator)
        if(self.numerator*(newDenominator/self.denominator) >= other.numerator*(newDenominator/other.denominator)):
            return True
        else:
            return False
            
    def __le__(self, other):
        newDenominator = LCM(self.denominator, other.denominator)
        if(self.numerator*(newDenominator/self.denominator) < other.numerator*(newDenominator/other.denominator)):
            return True
        else:
            return False
            
    def __mul__(self,other):
        return Fraction(self.numerator*other.numerator, self.denominator*other.denominator)
    
    def __truediv__(self,other):
        return Fraction(self.numerator*other.denominator, self.denominator*other.numerator)

testFraction = Fraction(5,12)
testFraction2 = Fraction(13,62)
listOfFractions = [Fraction(42,68),Fraction(21,64),Fraction(37,312),Fraction(36,21),Fraction(98,68),Fraction(31,57),Fraction(3,6),Fraction(2,3),Fraction(9,5),Fraction(37,56)]
print(MergeSort(listOfFractions))
print(testFraction*testFraction2, testFraction/testFraction2)