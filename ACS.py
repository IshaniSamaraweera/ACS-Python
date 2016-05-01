import math

class Node(object):
    
    def __init__(self):
        self.suffix_node = -1   

    def __repr__(self):
        return "Node(suffix link: %d)"%self.suffix_node

class Edge(object):
    
    def __init__(self, first_char_index, last_char_index, source_node_index, dest_node_index):
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        self.source_node_index = source_node_index
        self.dest_node_index = dest_node_index
        
    @property
    def length(self):
        return self.last_char_index - self.first_char_index

    def __repr__(self):
        return 'Edge(%d, %d, %d, %d)'% (self.source_node_index, self.dest_node_index 
                                        ,self.first_char_index, self.last_char_index )


class Suffix(object):
    
    def __init__(self, source_node_index, first_char_index, last_char_index):
        self.source_node_index = source_node_index
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        
    @property
    def length(self):
        return self.last_char_index - self.first_char_index
                
    def explicit(self):
        
        return self.first_char_index > self.last_char_index
    
    def implicit(self):
        return self.last_char_index >= self.first_char_index

        
class SuffixTree(object):
    
    def __init__(self, string, case_insensitive=False):
        
        self.string = string
        self.case_insensitive = case_insensitive
        self.N = len(string) - 1
        self.nodes = [Node()]
        self.edges = {}
        self.active = Suffix(0, 0, -1)
        if self.case_insensitive:
            self.string = self.string.lower()
        for i in range(len(string)):
            self._add_prefix(i)
    
    def __repr__(self):
        
        curr_index = self.N
        s = "\tStart \tEnd \tSuf \tFirst \tLast \tString\n"
        values = self.edges.values()
        values.sort(key=lambda x: x.source_node_index)
        for edge in values:
            if edge.source_node_index == -1:
                continue
            s += "\t%s \t%s \t%s \t%s \t%s \t"%(edge.source_node_index
                    ,edge.dest_node_index 
                    ,self.nodes[edge.dest_node_index].suffix_node 
                    ,edge.first_char_index
                    ,edge.last_char_index)
                    
            
            top = min(curr_index, edge.last_char_index)
            s += self.string[edge.first_char_index:top+1] + "\n"
        return s
            
    def _add_prefix(self, last_char_index):
        
        last_parent_node = -1
        while True:
            parent_node = self.active.source_node_index
            if self.active.explicit():
                if (self.active.source_node_index, self.string[last_char_index]) in self.edges:
                    # prefix is already in tree
                    break
            else:
                e = self.edges[self.active.source_node_index, self.string[self.active.first_char_index]]
                if self.string[e.first_char_index + self.active.length + 1] == self.string[last_char_index]:
                    # prefix is already in tree
                    break
                parent_node = self._split_edge(e, self.active)
        

            self.nodes.append(Node())
            e = Edge(last_char_index, self.N, parent_node, len(self.nodes) - 1)
            self._insert_edge(e)
            
            if last_parent_node > 0:
                self.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node
            
            if self.active.source_node_index == 0:
                self.active.first_char_index += 1
            else:
                self.active.source_node_index = self.nodes[self.active.source_node_index].suffix_node
            self._canonize_suffix(self.active)
        if last_parent_node > 0:
            self.nodes[last_parent_node].suffix_node = parent_node
        self.active.last_char_index += 1
        self._canonize_suffix(self.active)
        
    def _insert_edge(self, edge):
        self.edges[(edge.source_node_index, self.string[edge.first_char_index])] = edge
        
    def _remove_edge(self, edge):
        self.edges.pop((edge.source_node_index, self.string[edge.first_char_index]))
        
    def _split_edge(self, edge, suffix):
        self.nodes.append(Node())
        e = Edge(edge.first_char_index, edge.first_char_index + suffix.length, suffix.source_node_index, len(self.nodes) - 1)
        self._remove_edge(edge)
        self._insert_edge(e)
        self.nodes[e.dest_node_index].suffix_node = suffix.source_node_index  ### need to add node for each edge
        edge.first_char_index += suffix.length + 1
        edge.source_node_index = e.dest_node_index
        self._insert_edge(edge)
        return e.dest_node_index

    def _canonize_suffix(self, suffix):
        
        if not suffix.explicit():
            e = self.edges[suffix.source_node_index, self.string[suffix.first_char_index]]
            if e.length <= suffix.length:
                suffix.first_char_index += e.length + 1
                suffix.source_node_index = e.dest_node_index
                self._canonize_suffix(suffix)
 

    # Public methods
    def find_substring(self, substring):
        
        if not substring:
            return -1
        if self.case_insensitive:
            substring = substring.lower()
        curr_node = 0
        i = 0
        while i < len(substring):
            edge = self.edges.get((curr_node, substring[i]))
            if not edge:
                return -1
            ln = min(edge.length + 1, len(substring) - i)
            if substring[i:i + ln] != self.string[edge.first_char_index:edge.first_char_index + ln]:
                return -1
            i += edge.length + 1
            curr_node = edge.dest_node_index
        return edge.first_char_index - len(substring) + ln
        
    def has_substring(self, substring):
        return self.find_substring(substring) != -1

#create an array and import data files to it
fileArray = []
def importfileArray():
    for i in range(20): 
        name = str(i+1)+".txt"
        file = open(name,"r")
        File= file.read().replace("\n", "")
        fileArray.append(File)

importfileArray()

#create an array and insert suffix trees to it       
treeArray = []
def importTrees():
    for j in range(20):
        treeArray.append(SuffixTree(fileArray[j]))

importTrees()

def readFile():
    p = 0
    while p<20:
        q=0
        while q<20:
            if(p==q):
                total1 = (len(fileArray[p])/2)*(len(fileArray[p])+1)
                ansArray[p][q] = total1/len(fileArray[p])
            else:
                total2 = 0
                j=1
                for i in range(len(fileArray[p])):
                    while(treeArray[q].find_substring(fileArray[p][i:j]) != -1 and j<len(fileArray[p])+1):
                        j += 1
                    total2 += (len(fileArray[p][i:j])-1)
                    if(j>i+2):
                        j -= 1
                    else:
                        j = i+2
                        
                ansArray[p][q] = total2/len(fileArray[p])
                q +=1
        p +=1
                
ansArray = [[0 for x in range(20)] for x in range(20)]
acsArray = [[0 for x in range(20)] for x in range(20)]

#function to calculate values
def calculate():
    print("Please wait.! \nACS values are calculating...")
    readFile()

    i=0
    while i<20:
        j=0
        while j<20:
            #calculate the Average of The longest common substrings
            L = ansArray[i][j]
            L1 = ansArray[j][i]
            
           #calculate similarity measure among strings
            S = L/math.log(len(fileArray[j]),10)
            S1 = L1/math.log(len(fileArray[i]),10)
    
            #calculate distance measure (D) among strings
            D = (1/S)-(math.log(len(fileArray[i]),10)/ansArray[i][i])
            D1 = (1/S1)-(math.log(len(fileArray[j]),10)/ansArray[j][j])

            #calculate the final ACS measure
            ACS = (D+D1)/2
            acsArray[i][j] = ACS
            j+=1
        i+=1
            
    for i in range(0,20):
        for j in range(0,20):
            print("\nACS value of Textfile " + str(i+1) + " with Textfile " + str(j+1) + " = " + str(acsArray[i][j]))
  
calculate()


    







    
