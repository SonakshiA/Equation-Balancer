import re
from sympy import Matrix, lcm
list_elements=[]
elementMatrix=[]
temp_list=()

def matrix(element,index,count,side):
    if(index==len(elementMatrix)):
        elementMatrix.append([])
        for x in list_elements:
            elementMatrix[index].append(0)
    if (element not in list_elements):
        list_elements.append(element)
        for i in range(len(elementMatrix)):
            elementMatrix[i].append(0)
    col=list_elements.index(element)
    elementMatrix[index][col]+=count*side


def individualElement(segment,index,subscript,side):
    elements=re.split('([A-Z][a-z]?)',segment)
    i=0
    while(i<len(elements)-1):
        i+=1
        if (len(elements[i])>0):
            if(elements[i+1].isdigit()):
                count=int(elements[i+1])*subscript
                matrix(elements[i],index,count,side)
                i+=1
            else:
                matrix(elements[i],index,subscript,side)
    
    
def compoundFormation(compound,index,side):
    segments=re.split('(\([A-Za-z0-9]*\)[0-9]*)',compound)
    for segment in segments:
        if segment.startswith("("):
            segment=re.split('\)([0-9]*)',segment)
            subscript=int(segment[1])
            segment=segment[0][1:] 
        else:
            subscript=1 # if monoatomic
        individualElement(segment,index,subscript,side) 


reactants=input("Enter your reactants: ").split('+')
products=input("Enter your products: ").split('+')
print('\n')

for i in range(len(reactants)):
    compoundFormation(reactants[i],i,1)
    

for i in range(len(products)):
    compoundFormation(products[i],i+len(reactants),-1)
 

elementMatrix=Matrix(elementMatrix)
elementMatrix=elementMatrix.transpose()
solution=elementMatrix.nullspace()[0]
print(solution)


multiple=lcm([val.q for val in solution])
coeffs=[multiple*val for val in solution]

for i in range(len(reactants)-1):
    print(str(coeffs[i])+reactants[i]+ ' + ',end='')
print(str(coeffs[len(reactants)-1])+reactants[-1]+ ' -> ',end='')


for j in range(len(products)-1):
    print(str(coeffs[len(reactants)+j])+products[j]+ ' + ',end='')
print(str(coeffs[-1])+products[-1])


