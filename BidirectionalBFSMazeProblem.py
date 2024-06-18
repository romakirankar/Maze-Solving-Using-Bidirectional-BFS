from tkinter import filedialog
from collections import deque

class SolveMaze:
    def __init__(self):
        self.matrix = []
        self.entranceQueue = []
        self.exitQueue = []
        self.visitedEntrances=[]
        self.visitedExits=[]
        self.uploadFile()
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])
        self.searchPath()
  
    def uploadFile(self):
        actionRead = "r"
        try:
            filePathInput = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if filePathInput:
                with open(filePathInput, actionRead) as fileContent:
                    self.matrix = [list(map(int, line.strip().rstrip('\n').replace(' ', ''))) for line in fileContent]
       
        except Exception as err:
            print(f"Some error occured in uploading file: {err}")

    def writeFile(self):
        try:
            with open("OutputMaze.txt", "w") as file:
                for iRow in range(len(self.matrix) - 1):
                    file.write(''.join(map(str, self.matrix[iRow])) + '\n')
                file.write(''.join(map(str, self.matrix[-1])))  # Remove the last newline
            print("Data was written successfully in file OutputMaze.txt")
        
        except Exception as e:
            print(f"Error occurred in saving: {e}")

    #Executes for both entrance and exit side search
    def checkNextMove(self, queue, visited, newRow, newCol):
        if 0 <= newRow < self.rows and 0 <= newCol < self.columns and self.matrix[newRow][newCol] == 0:
            queue.append((newRow, newCol))
            visited.append((newRow, newCol))

    def searchPath(self):
        pathFound = False
        self.entranceQueue= deque([(0, 0)])
        self.exitQueue = deque([(self.rows - 1, self.columns - 1)])
        self.visitedEntrances = [(0, 0)]
        self.visitedExits = [(self.rows - 1, self.columns - 1)]

        while self.entranceQueue and self.exitQueue:
            
        # Process nodes from entrance side
            presentCoordinates = self.entranceQueue.popleft()
            
            if presentCoordinates in self.visitedExits:
                pathFound = True
                meetingPoint = presentCoordinates
                break  # Path found

            #Move Down
            newRow = presentCoordinates[0] + 1
            newCol = presentCoordinates[1]

            if(newRow, newCol) not in self.visitedEntrances: #no revisit of the same coordinates from entrance side
                self.checkNextMove(self.entranceQueue, self.visitedEntrances, newRow, newCol)

            #Move Right
            newRow = presentCoordinates[0]
            newCol = presentCoordinates[1] + 1

            if(newRow, newCol) not in self.visitedEntrances: #no revisit of the same coordinates from entrance side
                self.checkNextMove(self.entranceQueue, self.visitedEntrances, newRow, newCol)


        # Process nodes from exit side
            presentCoordinates = self.exitQueue.popleft()
            
            if presentCoordinates in self.visitedEntrances:
                pathFound = True
                meetingPoint = presentCoordinates
                break  # Path found

            #Move Up
            newRow = presentCoordinates[0] - 1
            newCol = presentCoordinates[1]

            if(newRow, newCol) not in self.visitedExits: #no revisit of the same coordinates from exit side
                self.checkNextMove(self.exitQueue, self.visitedExits, newRow, newCol)
            
            #Move Left
            newRow = presentCoordinates[0]
            newCol = presentCoordinates[1] - 1

            if(newRow, newCol) not in self.visitedExits: #no revisit of the same coordinates from exit side
                self.checkNextMove(self.exitQueue, self.visitedExits, newRow, newCol)

        # Upon findind a path,
        if pathFound:

            #Backtrack from meeting point to entrance marking the path as 2
            currentPoint = meetingPoint

            while currentPoint != (0, 0):
                row, col = currentPoint
                self.matrix[row][col] = 2
                
                if currentPoint in self.visitedEntrances:
                    if (row - 1, col) in self.visitedEntrances:
                        currentPoint = (row - 1, col)  
                    else:
                        currentPoint = (row, col - 1)
               
            #Mark the entrance as 2 since it was skipped in the loop
            self.matrix[0][0] = 2 

            #Go from meeting point to exit marking the path as 2
            currentPoint = meetingPoint

            while currentPoint != (self.rows-1, self.columns-1):
                row, col = currentPoint
                self.matrix[row][col] = 2

                if currentPoint in self.visitedExits:
                    if (row + 1, col) in self.visitedExits:
                        currentPoint = (row + 1, col)  
                    else:
                        currentPoint = (row, col + 1)
            
            #Mark the exit as 2 since it was skipped in the loop
            self.matrix[self.rows-1][self.columns-1] = 2 

            #Write the output file with the updated matrix
            self.writeFile()
        else:
            print('No path found! Thus, no output file was generated.')

SM = SolveMaze()