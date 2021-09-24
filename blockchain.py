import datetime
import hashlib
import threading

class Block:
    data = None
    previousHash = None
    currentHash = None
    timeStamp = None
    nextBlock = None
    blockNumber = 0
    nonce = 0

    def __init__(self,data,timeStamp):
        self.data = data
        self.timeStamp = timeStamp

    def hash(self):
        h = hashlib.sha256()
        h.update(str(self.nonce).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previousHash).encode('utf-8') + str(self.timeStamp).encode('utf-8') + str(self.blockNumber).encode('utf-8'))
        return h.hexdigest()
    
    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNumber) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\nTimeStamp: " + str(self.timeStamp) +"\n--------------"      

class Blockchain:

    diff = 20
    maxNonce = 2**32
    target = 2 ** (256-diff)
    block = Block("Genesis",datetime.datetime.now())
    dummy = head = block

    def add(self, block):

        block.previousHash = self.block.hash()
        block.blockNumber = self.block.blockNumber + 1

        self.block.nextBlock = block
        self.block = self.block.nextBlock


    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print("Block " + str(block.blockNumber) + " added to verified pool in background")
                break
            else:
                block.nonce += 1

class TransactionQueue:

    block = Block("Q",datetime.datetime.now())
    dummy = head = block

    def add(self, block):

        self.block.nextBlock = block
        self.block = self.block.nextBlock

verified_pool = Blockchain()
unverified_pool = TransactionQueue()
choice=-1
done=0

def verifyBlock():
    global unverified_pool
    global verified_pool
    global done
    while(done==0):
        while(unverified_pool.head!=None and done==0):
            
            if(unverified_pool.head!=unverified_pool.dummy):
                verified_pool.mine(Block(unverified_pool.head.data,unverified_pool.head.timeStamp))
                while(unverified_pool.head == unverified_pool.block and done==0):
                    pass
            if(unverified_pool.head.nextBlock!=None):
                unverified_pool.head = unverified_pool.head.nextBlock

t1 = threading.Thread(target = verifyBlock, args = ())
t1.start()

while(choice!=0):

    print("Enter choice:\n1.Add transaction\n2.Show verified transaction\n3.Exit")
    choice = int(input())

    if(choice == 1):

        amount = input("Enter amount: ")
        unverified_pool.add(Block(amount,datetime.datetime.now()))

    elif(choice == 2):

        start = verified_pool.dummy
        while start!=None:
            print(start)
            start = start.nextBlock

    elif(choice == 3):

        break

    else:

        print("Incorrect choice")

done = 1
t1.join()
    
