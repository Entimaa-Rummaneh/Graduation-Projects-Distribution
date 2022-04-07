from Group import *
from Project import *
from Chromosome import *
import random
import copy
import xlwt
import xlrd

groups = []
projects = []
chromosomes = []


def readGroupsFile(groups):
    # Reading the groups file and creating objects of them
    f = open("StudentsSelections.txt", "r+")
    for line in f:
        if line == '\n':
            continue
        else:
            l = (line.split(";"))
            groupnum = int(l[0])
            students = l[1]
            selection1 = int(l[2])
            selection2 = int(l[3])
            selection3 = int(l[4])
            group = Group(groupnum, students, selection1, selection2, selection3)
            groups.append(group)


def readProjectssFile(projects):
    # Reading the projects file and creating objects of them
    f = open("Projects.txt", "r+")
    for line in f:
        if line == '\n':
            continue
        else:
            l = (line.split(";"))
            projectnum = int(l[0])
            supervisor = l[1]
            title = l[2]
            project = Project(projectnum, supervisor, title)
            projects.append(project)


def printGroups(groups):
    for group in groups:
        print(group.__str__())


def printProjects(projects):
    for project in projects:
        print(project.__str__())


def generateChromosome(projects):
    list = []
    projectsList = []
    for i in range(0, 36):
        projectsList.append("Empty")  # initializing the list

    list = random.sample(range(1, 39), 36)  # generate 36 distinct numbers for the projects

    for i in range(0, 36):  # put the projects in the chromosome as the order in list[]
        for proj in projects:
            if Project.getProjectnum(proj) == list[i]:
                projectsList[i] = proj
    # for project in projectsList:
    #    print(str(Project.getProjectnum(project)))
    Fitness = fitness(projectsList, groups)
    # print(Fitness)
    chromosome = Chromosome(projectsList, Fitness)
    return chromosome


def fitness(project, groups):
    fitnessValue = 0
    for i in range(0, 36):
        if Group.getSelection1(groups[i]) == Project.getProjectnum(project[i]):
            fitnessValue += 3
        elif Group.getSelection2(groups[i]) == Project.getProjectnum(project[i]):
            fitnessValue += 2
        elif Group.getSelection3(groups[i]) == Project.getProjectnum(project[i]):
            fitnessValue += 1
    return fitnessValue


def numgroups(project, groups):
    # calculate number of groups that have a project from their selections in a chromosome
    num = 0
    for i in range(0, 36):
        if Group.getSelection1(groups[i]) == Project.getProjectnum(project[i]) or Group.getSelection2(
                groups[i]) == Project.getProjectnum(project[i]) or Group.getSelection3(
                groups[i]) == Project.getProjectnum(project[i]):
            num += 1
    return num


def twomaxfitness(chromosomes):
    # pick best two chromosomes with higher fitness values for crossover
    maxOne = 0
    maxTwo = 0
    maxOneChromosome = 0
    maxTwoChromosome = 0
    for c in chromosomes:
        if maxOne < Chromosome.getFitness(c):
            maxTwo = maxOne
            maxTwoChromosome = maxOneChromosome
            maxOne = Chromosome.getFitness(c)
            maxOneChromosome = c
        else:
            if maxTwo < Chromosome.getFitness(c):
                maxTwo = Chromosome.getFitness(c)
                maxTwoChromosome = c
    # print(str(maxOne) +":"+str(Chromosome.getFitness(maxOneChromosome)) +"       "+str(maxTwo)+":"+str(Chromosome.getFitness(maxTwoChromosome)))
    # Chromosome.__str__(maxOneChromosome)
    return maxOneChromosome, maxTwoChromosome


def crossover(first_parent, second_parent):
    child_one = copy.deepcopy(first_parent)  # child one is a copy of parent one before crossover
    child_two = copy.deepcopy(second_parent)  # child two is a copy of parent two before crossover
    # Chromosome.__str__(child_one)
    # print("**********************************************************************************************************")
    # Chromosome.__str__(child_two)
    first_position = random.randint(0, 35)  # select random position in child one
    # print(first_position)
    num_one = Project.getProjectnum(child_one.list[first_position])
    # print("num: "+ str(num_one))
    second_position = random.randint(0, 35)  # select random position in child two
    num_two = Project.getProjectnum(child_two.list[second_position])
    # print(second_position)
    # swap between the two chromosomes
    gene = child_one.list[first_position]
    child_one.list[first_position] = child_two.list[second_position]
    child_two.list[second_position] = gene
    # check if children have a conflict after crossover
    check_conflict(child_one, num_one)
    check_conflict(child_two, num_two)
    # add children to chromosomes
    chromosomes.append(child_one)
    chromosomes.append(child_two)
    return child_one, child_two


def check_conflict(child, num):
    # try two options for the child if it has a conflict and choose the better one
    copy_child = copy.deepcopy(child)
    for i in range(0, len(child.list)):
        for j in range(i + 1, len(child.list)):
            if Project.getProjectnum(child.list[i]) == Project.getProjectnum(child.list[j]):
                proj = copy.deepcopy(child.list[i])

                for project in projects:
                    if num == Project.getProjectnum(project):
                        proj = project
                        # print(Project.__str__(proj))

                child.list[i] = proj
                fitness1 = fitness(child.list, groups)
                # print("fitness1: "+str(fitness1))
                copy_child.list[j] = proj
                fitness2 = fitness(copy_child.list, groups)
                # print("fitness2: " + str(fitness2))
                if fitness2 > fitness1:
                    child = copy_child
                # print("index: " + str(i) + " value: " + str(Project.getProjectnum(child.list[i])))
                # print("index: " + str(j) + " value: " + str(Project.getProjectnum(child.list[j])))

    child.fitness = fitness(child.list, groups)


def mutation(child):
    print("mutation occurs")
    # choose two positions on the chromosomes randomly
    first_position = random.randint(0, 35)
    second_position = random.randint(0, 35)
    # Chromosome.__str__(child)
    # print("**********************************************************************************************************")
    # swap between genes
    gene = child.list[first_position]
    child.list[first_position] = child.list[second_position]
    child.list[second_position] = gene
    # calculate the new fitness after the mutation
    child.fitness = fitness(child.list, groups)
    # Chromosome.__str__(child)


def export_to_excel(first):
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Output")

    styleA = xlwt.easyxf('font: name Calibri, color-index black, bold on, height 220;'
                         'align: horiz center, vert center;'
                         'pattern:pattern solid, fore_colour silver_ega;'
                         'border: left medium,top medium,right medium,bottom medium, top_color black, bottom_color black, right_color black, left_color black;')

    styleB = xlwt.easyxf('font: name Calibri, color-index white, bold on, height 220;'
                         'align: horiz center, vert center;'
                         'pattern:pattern solid, fore_colour indigo;'
                         'border: left medium,top medium,right medium,bottom medium, top_color black, bottom_color black, right_color black, left_color black;')

    styleC = xlwt.easyxf('font: name Calibri, color-index black, bold on, height 220;'
                         'align: horiz center, vert center;'
                         'pattern:pattern solid, fore_colour rose;'
                         'border: left medium,top medium,right medium,bottom medium, top_color black, bottom_color black, right_color black, left_color black;')

    row = 0
    col = 0
    dataCaps = ["Students", "Project", "Supervisor"]
    ws.write(row, col, dataCaps[0], styleC)
    ws.write(row, col + 1, dataCaps[1], styleC)
    ws.write(row, col + 2, dataCaps[2], styleC)
    row += 1
    groupnum = 0
    for group in first.list:
        col = 0
        if type(group) != str:
            ws.write(row, col, Group.getStudents(groups[groupnum]), styleA)
            ws.write(row, col + 1, Project.getTitle(group), styleB)
            ws.write(row, col + 2, Project.getSupervisor(group), styleA)
        row += 1
        groupnum += 1

    wb.save("output.xls")
    readerSheet = xlrd.open_workbook("output.xls").sheet_by_index(0)
    for row in range(readerSheet.nrows):
        for column in range(readerSheet.ncols):
            thisCell = readerSheet.cell(row, column)
            neededWidth = int((1 + len(str(thisCell.value))) * 200)
            if ws.col(column).width < neededWidth:
                ws.col(column).width = neededWidth
    wb.save("output.xls")


def main():
    counter = 0
    groups.clear()
    projects.clear()
    chromosomes.clear()
    readGroupsFile(groups)
    readProjectssFile(projects)
    # generate some initial chromosomes
    for i in range(0, 30):
        chromosomes.append(generateChromosome(projects))

    # for c in chromosomes:
    #    print(str(Chromosome.getFitness(c)))
    goal_fitness = 60  # 69
    max_fitness = 0
    emptylist = []
    emptyfitness = 0
    first = Chromosome(emptylist, emptyfitness)

    while max_fitness < goal_fitness:
        # print(counter)
        counter += 1
        # restart if more than 4000 loops
        if counter > 4000:
            print("============================")
            print("         RESTART")
            print("============================")
            main()

        first, second = twomaxfitness(chromosomes)
        # print("Parent 1 fitness: "+ str(first.getFitness()) + "          Parent 2 fitness: "+ str(second.getFitness()))
        max_fitness = Chromosome.getFitness(first)
        print("max fitness: " + str(max_fitness))
        childone, childtwo = crossover(first, second)
        ratio = 0.2
        randnum = random.random()
        if ratio > randnum:
            mutation(childone)
            mutation(childtwo)
        ratio = ratio - (ratio * 0.01)

        # print("Child 1 fitness: " + str(childone.getFitness()) + "          Child 2 fitness: " + str(childtwo.getFitness()))
        print("***********************")
    # print("max: "+str(max_fitness))
    # Chromosome.__str__(first)
    return first, max_fitness


first, max_fitness = main()
print("max: " + str(max_fitness))
num_of_groups = numgroups(first.list, groups)
print("num of groups have a project from their selections: " + str(num_of_groups))
export_to_excel(first)
