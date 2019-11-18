

class PriorityQueue(list):

##    def Len(pq):
##	return len(pq)

    def Less(pq, i, j):
	return pq[i].Error() < pq[j].Error()

    def Swap(pq, i, j):
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].Index = i
	pq[j].Index = j

    def Push(pq, x):
	item = x
	item.Index = len(pq)
	pq.append(item)

    def Pop(pq):
	item = pq.pop(-1)
	item.Index = -1
	return item
