import datetime
import hashlib
class Block:
    data = None
    previousHash = None
    currentHash = None
    timeStamp = None
    nextBlock = None
    blockNumber = 0
    nonce = 0

    def __init__(self,data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(str(self.nonce).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previousHash).encode('utf-8') + str(self.timeStamp).encode('utf-8') + str(self.blockNumber).encode('utf-8'))
        return h.hexdigest()
    
    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNumber) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"      

class Blockchain:

    diff = 20
    maxNonce = 2**32
    target = 2 ** (256-diff)
    block = Block("Genesis")
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
                print(block)
                break
            else:
                block.nonce += 1

blockchain = Blockchain()
choice=-1
while(choice!=0):
    print("Enter choice:\n1.Add transactionn\n2.Show transaction\n3.Exit")
    choice = int(input())
    if(choice == 1):
        amount = input("Enter amount: ")
        blockchain.mine(Block(amount))
    elif(choice == 2):
        while blockchain.head != None:
            print(blockchain.head)
            blockchain.head = blockchain.head.nextBlock
        blockchain.head = blockchain.dummy
    elif(choice == 3):
        break
    else:
        print("Incorrect choice")


    
