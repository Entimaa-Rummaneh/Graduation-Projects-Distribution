class Group:
    def __init__(self,groupnum, students, selection1, selection2, selection3):
        self.groupnum = groupnum
        self.students = students
        self.selection1 = selection1
        self.selection2 = selection2
        self.selection3 = selection3

    def __str__(self):
        return "Num: "+str(self.groupnum)+", Names: " + self.students + ", Selections=" + str(self.selection1) + ", " + str(
            self.selection2) + ", " + str(self.selection3)

    def getSelection1(self):
        return self.selection1

    def getSelection2(self):
        return self.selection2

    def getSelection3(self):
        return self.selection3

    def getStudents(self):
        return self.students