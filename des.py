import heapq
q = []
heapq.heapify(q)
def queuePrinter():
    for i in q:
        print(" ",i[0],i[1].__name__,end=" ")
        for j in i[2:]:
            print(j,end=" ")
        print()
'''q=[]
class heapq:
    @staticmethod
    def heappush(li,item):
        li.append(item)

    @staticmethod
    def heappop(li):
        min=li[0]
        min_index=0
        for i in range(len(li)):
            if li[i].timestamp<min.timestamp:
                min=li[i]
                min_index=i
        val=li.pop(min_index)
        return val
'''