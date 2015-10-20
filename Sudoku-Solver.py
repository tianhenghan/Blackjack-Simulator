#The code reads in a sudoku from an external file and solve it using Algorithm X.
#The total time spent on the problem is shown.

import time
import decimal
import pprint

# delete columns and rows specified in each iteration of Algorithm X. tab[y][x] represents
# an evolving two-dimensional matrix. xsl/ysl is a list of x/y indices of columns/rows to be deleted.
def dele(tab,xsl,ysl):

	for y in ysl: tab.pop(y)
	
	for x in xsl: 
	
		for y in range(len(tab)): 	tab[y].pop(x)
		
	return tab
	

# recursion. sol pass partially solution and is saved into solution if successful.
def solve(tab, sol, solution):

	yr=len(tab)
	xr=len(tab[0])

	# base of recursion, solution found.
	if yr==1:
	
		solution.append(sol)
		
		return solution		
		
	else:
		total = [ sum(tab[y]) - tab[y][xr-1]    for y in range(yr-1) ]
		minvalue = min(total)
		
		# base of recursion, failed branch.		
		if minvalue==0: 
		
			return solution

		# continue with Algorithm X by finding the xsl and ysl for the next level.
		# tab[y][:] and sol[:] are passed for recursion to keep their values at the current level.
		else:
			miny=total.index(minvalue)
			
			for x in range(xr-1):
			
				if tab[miny][x]==1:
				
					xs=set()
					ys=set()
					
					xs.add(x)
					sol.append(tab[yr-1][x])
					
					for y in range(yr-1):		
							
						if tab[y][x]==1:
						
							ys.add(y)
							
							for xx in range(xr-1):	
										
								if tab[y][xx]==1: 	xs.add(xx)
									
					xsl=list(xs)					
					ysl=list(ys)
					
					xsl.sort(reverse=True)
					ysl.sort(reverse=True)
					
					solution = solve(dele([tab[y][:] for y in range(yr)],xsl,ysl),sol[:],solution)
					
			return solution


# make starting 325 x 730 matrix, load the sudoku puzzle and initialize the matrix before calling solve().
start=decimal.Decimal(time.time())

tab = [[0 for x in range(730)] for y in range(325)]

for x in range(729):

	tab[x//9][x]=1
	
	tab[(x//81)*9+x%9+81][x]=1
	
	tab[x%81+162][x]=1
	
	tab[(x//243)*27+((x//27)%3)*9+x%9+243][x]=1
	
for x in range(729): 	tab[324][x]=x

for y in range(324): 	tab[y][729]=y

f=open('puzzles.txt')
txt=f.read()

nums = [ txt[i]  for i in range(len(txt)) if txt[i].isdigit() or txt[i]=='.']

f.close()

puzzle = [ [ 0  for i in range(9)]  for j in range(9)]

for k in range(81):

	if nums[k]!='.': 	puzzle[k//9][k%9]=int(nums[k])

print '\n',' '*10,'puzzle\n'
pprint.pprint(puzzle)

xs=set()
ys=set()

for i in range(9):

	for j in range(9):
	
		if puzzle[i][j]!=0:
		
			x=i*81+j*9+puzzle[i][j]-1
			xs.add(x)
			
			for y in range(324):	
						
				if tab[y][x]==1: 
				
					ys.add(y)
					
					for xx in range(729):	
								
						if tab[y][xx]==1: 	xs.add(xx)

xsl=list(xs)
ysl=list(ys)

xsl.sort(reverse=True)
ysl.sort(reverse=True)

solution=[]
sol=[]

solution = solve(dele(tab,xsl,ysl),sol,solution)

if len(solution)==0: 	print '\n',' '*5,'No solution exist!'

else:
	for n in range(len(solution)):
	
		for s in range(len(solution[n])): 
		
			puzzle[solution[n][s]//81][(solution[n][s]%81)//9] = (solution[n][s]%81)%9+1
			
		print '\n',' '*8,'solution',n+1,'\n'
		pprint.pprint(puzzle)

end=decimal.Decimal(time.time())
print '\ntotal solving time:',end-start,'seconds\n'