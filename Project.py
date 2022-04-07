class Project:
    def __init__(self,project_num, supervisor, title):
        self.project_num = project_num
        self.supervisor = supervisor
        self.title = title

    def __str__(self):
        return "Num: "+str(self.project_num)+", Supervisor: " + self.supervisor + ", Title:" + str(self.title)

    def getProjectnum(self):
        return self.project_num

    def getTitle(self):
        return self.title

    def getSupervisor(self):
        return self.supervisor
