class Node:
    def __init__(self, key):
        self.key = key
        self.right = self.left = None
        self.height  = 0

    def __str__(self):
        return f"{self.key}"

    
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insertBST(self, new_key):
        self.p = self.root
        self.q = None
        new_node = Node(new_key)
        
        if self.p is None:
            self.root = new_node
            return True
            
        while self.p:
            if new_key == self.p.key:
                ## “i <key> : The key already exists”을 따옴표를 제외하고 한줄에 출력
                ## <key>에는 입력으로 주어진 키값을 출력    
                print(f"i {new_key} : The key already exists")
                return 

            self.q = self.p

            if new_key < self.q.key:
                self.p = self.q.left
            else:
                self.p = self.q.right

        ## 현재 self.p == None인 상태이고, self.q == 단말노드, self.q 밑에 new_node를 추가해야함
        ## self.q.left에 추가
        if new_key < self.q.key:
            self.q.left = new_node
        else:
            self.q.right = new_node

        ## height 새로 갱신
        self.update_height()
        ## end of insertBST
            
        print(self.print_inorderBST(self.root))
    
    
    def cal_height_node(self,node):
        if node is None:
            return 0
        else:
            left_height = self.cal_height_node(node.left)
            right_height = self.cal_height_node(node.right)

            if (left_height > right_height):
                return left_height + 1
            else:
                return right_height +1

    def cal_height_key(self, key):
        node = self.searchBST(key)
        return self.cal_height_node(node)
        

    def searchBST(self, key):
        self.p = self.root
        while self.p:
            if self.p.key == key:
                return self.p
            elif self.p.key > key:
                if self.p.left is not None:
                    self.p = self.p.left
                else:
                    print("there is no node in the tree")
                    return False
            elif self.p.key < key:
                if self.p.right is not None:
                    self.p = self.p.right
                else:
                    print("there is no node in the tree")
                    return False


    def deleteBST(self, delete_key):
        self.q = None
        self.p = self.root

        while self.p is not None and self.p.key != delete_key:
            self.q = self.p
            if delete_key < self.p.key:
                self.p = self.p.left
            else:
                self.p = self.p.right
        ## end while    
        
        ## 끝까지 내려갔는데 delete_key가 없을 때
        if self.p is None:   
            print(f"d {delete_key} : The key does not exist")
            return  

        # self.p는 delete_node이고,
        # self.q는 delete_node의 parent node이다.

        if self.p.left is not None and self.p.right is not None:
            temp_node = self.p     ## temp_node == delete_node == self.p

            ## 오른쪽 서브노드의 height가 더 클 때 
            ## 오른쪽에서 가장 작은 노드로 대체함.
            ## min_node(temp.p.right)를 통해
            ## 위의 노드의 부모가 이 노드를 삭제해야함
            
            if self.cal_height_node(self.p.left) < self.cal_height_node(self.p.right):
                self.p = self.minNode(self.p.right)
                
            elif self.cal_height_node(self.p.left) > self.cal_height_node(self.p.right):
                self.p = self.maxNode(self.p.left)

            else:
                if self.noNodes(self.p.left) >= self.noNodes(self.p.right):
                    self.p = self.maxNode(self.p.left)
                else:
                    self.p = self.minNode(self.p.right)

            ## 조건에 따라서 현재 self.p는 
            ## left에서 가장 큰 값이거나, right에서 가장 큰 작은 값이거나 
            ## self.q는 현재 delete_node의 parent node

            ## self.p의 부모는 parent_node가 받고있음
            self.q = self.parentBST(self.p)
            
            ## 현재 self.p의 degree는 0 or 1
            ## self.p를 삭제해야하고, self.p의 부모와 self.p의 자식을 이어주어야한다.
        
            # self.p의 차수가 0
            if self.p.left is None and self.p.right is None:
                if self.q is None:
                    self.root = None
                elif self.q.left == self.p:
                    self.q.left = None
                    temp_node.key = self.p.key
                else:
                    self.q.right = None
                    temp_node.key = self.p.key

            # self.p의 차수가 1
            elif self.p.left is not None and self.p.right is None:
                if self.q is None:
                    self.root = None
                elif self.p == self.q.left:
                    if self.p == self.maxNode(self.p):
                        self.q.left = self.p.left
                    else:
                        self.q.left = self.p.right
                    temp_node.key = self.p.key
                else:
                    if self.p == self.minNode(self.p):
                        self.q.right = self.p.right
                    else:
                        self.q.right = self.p.left
                    temp_node.key = self.p.key

            elif self.p.left is None and self.p.right is not None:
                if self.q is None:
                    self.root = None
                elif self.q.left == self.p:
                    if self.p == self.maxNode(self.p):
                        self.q.left = self.p.left
                    else:
                        self.q.left = self.p.right
                    temp_node.key = self.p.key
                else:
                    if self.p == self.minNode(self.p):
                        self.p.right = self.p.left
                    else:
                        self.q.right = self.p.left
                    temp_node.key = self.p.key
            else:
                print(f"Error: 대체할 노드가 제대로 선정되지 않음 : {self.p}")

        ## 삭제하려는 노드의 차수가 2가 아닌 경우
        ## 왼쪽 자식노드만 있는 경우 
        elif self.p.left is not None and self.p.right is None:
            if self.p == self.root:
                self.root = self.p.left
            elif self.q.right == self.p:
                self.q.right = self.p.left
            else:
                self.q.left = self.p.left

        ## 오른쪽 자식 노드만 있는 경우
        elif self.p.left is None and self.p.right is not None:
            if self.p == self.root:
                self.root = self.p.right
            elif self.q.right == self.p:
                self.q.right = self.p.right
            else:
                self.q.left = self.p.right

        ## 삭제하려는 노드의 자식이 하나도 없는 경우
        else:    
            if self.p == self.root:
                self.root = None
            elif self.q.left == self.p:
                self.q.left = None
            else:
                self.q.right = None
        
        ## 삭제 완료 후 모든 노드들의 height 갱신
        self.update_height()
        ### end of deleteBST 
        print(self.print_inorderBST(self.root))

    
    def update_height(self):
        node_list = self.inorderBST(self.root)
        for i in node_list:
            self.searchBST(i).height = self.cal_height_node(self.searchBST(i))


    def inorderBST(self, node):
        return_list = []
        if node:
            return_list = self.inorderBST(node.left) # 계속 타고 내려가면서 가장 키 값이 낮은 노드에 접근
            return_list.append(node.key) 
            return_list = return_list + self.inorderBST(node.right)
        return return_list


    def print_inorderBST(self, node):
        ret_list = self.inorderBST(node)
        ret = ""
        for i in ret_list:
            ret += str(i) + " "
        return ret
        

    def noNodes(self, node):
        # 특정 노드를 루트로 했을 때 서브트리에 있는 노드의 개수
        return len(self.inorderBST(node)) - 1


    def maxNode(self, node):
        # 서브노드에서 가장 큰 키를 가진 노드 return
        max_node = node
        while max_node.right:
            max_node = max_node.right
        return max_node
                  

    def minNode(self, node):
        # 서브노드에서 가장 작은 키를 가진 노드 return
        min_node = node
        while min_node.left:
            min_node = min_node.left
        return min_node


    def parentBST(self, node):
        ## 파라미터로 들어오는 node의 parent를 구하는 함수
        parent = None
        target = self.root

        while target != node:
            parent = target
            if target.key < node.key:
                target = target.right
            else:
                target = target.left
        return parent



## insert/delete 처리를 마친 후 트리 순회 결과를 한줄에 출력한다. 
## 키 값 사이에 공백을 두고 출력함

bst = BinarySearchTree()
input_list = []

f = open("/Users/bk/Desktop/Dev/3-2/File-Process/Tree/bst/bst_input.txt", 'r')
while True:
    line = f.readline()
    if not line:
        break
    input_list.append(line.split())
f.close()

for i in input_list:
    i[1] = int(i[1])


for i in input_list:
    # print(f"i : {i[1]}=>", end = " ")
    if i[0] == 'i':
        bst.insertBST(i[1])
    elif i[0] == "d":
        bst.deleteBST(i[1])
    else:
        raise Exception(f"Invalid input : {i[0]}")