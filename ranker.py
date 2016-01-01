'''
Created on 28 Oct 2015

@author: tobydobbs
'''

#===============================================================================
# function used to sort mses (mean-standard errors) ranking them from best to worst
#===============================================================================
def quickSort(array_tuples, lo, hi):
    if lo < hi:
        p = partition(array_tuples, lo, hi)
        quickSort(array_tuples, lo, p - 1)
        quickSort(array_tuples, p + 1, hi)

#===============================================================================
# partition: partition each array into sub-arrays: notice use of descending order
#===============================================================================
def partition(array_tuples, lo, hi):
    wall = lo
    pivot = hi
    for i in range(lo, hi):
        if array_tuples[i][1] > array_tuples[pivot][1]:
            swap(array_tuples, wall, i)
            wall += 1 # move the wall up one space
    swap(array_tuples, wall, hi)
    return wall
            
#===============================================================================
# swap: swaps two elements within an array
#===============================================================================
def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp
    
def main():
    array = [(-15,7), (1,2), (2,1), (4,3)]
    quickSort(array, 0, len(array)-1)
    print array
    
if __name__ == "__main__":
    main()
        
        
