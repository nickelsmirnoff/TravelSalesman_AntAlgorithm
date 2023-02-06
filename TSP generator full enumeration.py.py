import random as rnd
import itertools as it
import os
#Будем решать задачу коммивояжера с N городов

def DistMatrixGenerator(N,min,max):
    #функция создания матрицы расстояний размера N на N. Диапазон расстояний от min до max
    matr = [[0 for i in range(N)] for j in range(N)]
    #создали матрицу N на N и заполнили нулями
    for i in range(N):
        for j in range(i+1,N):
            matr[i][j] = rnd.randint(min,max)
            matr[j][i] = matr[i][j]
    for i in range(len(matr)):
        print(matr[i])
    #Заполнили матрицу расстояниями между городами. Матрица симметрична относительно главной диагонали
    print(" ↑ distance matrix")
    print()
    return matr

def StartPermutation(N):
    #функция создания начальной перестановки для N городов
    res = [0]
    for i in range(1,N):
        res.append(i)
    res.append(0)
    # print(res)
    # print("↑ start permutation")
    # print()
    return res

def CountRoute(Perm,Matr):
    #функция подсчета расстояния, пройденного коммивояжером по маршруту Perm для матрицы Matr
    dist = 0
    for i in range(0,len(Perm)-1):
        # print("route =",Perm[i],Perm[i+1],", distance =",Matr[Perm[i]][Perm[i+1]])
        dist += Matr[Perm[i]][Perm[i+1]]
    #print(Perm[len(Perm)])
    # print(Perm)
    # print("↑ current permutation Distance =",dist)
    #print()
    return dist

def GenerateAllRoutes(Perm):
    #функция генерации всех маршрутов для коммивояжера (перестановок городов) на основе начального маршрута Perm
    CutPerm = Perm.copy() #копируем начальную перестановку, чтобы не испортить ее
    CutPerm.pop(len(CutPerm)-1) #удаляем нули по краям перестановки. в задаче старт маршрута всегда в городе номер 0
    CutPerm.pop(0) #переставлять будем элементы Perm без нулевого города
    temp = it.permutations(CutPerm)
    resultArray = []
    for p in temp:
        # print(p)
        tempString = [0]
        for i in p:
            tempString.append(i)
        tempString.append(0)
        # print(tempString)
        resultArray.append(tempString)

    return resultArray

def FullTaskSolver(N,min,max): #функция решения задачи коммивояжера полным перебором для N городов
    #расстояния между городами в диапазоне от min до max
    DistMatr = DistMatrixGenerator(N, min, max)  # создаем матрицу расстояний
    SP = StartPermutation(N)  # создаем начальный маршрут
    AllRoutes = GenerateAllRoutes(SP)  # генерируем все маршруты
    print("all routes generated:", len(AllRoutes), "at all with", N, "cities")
    BestRoute = SP
    BestRouteDist = CountRoute(BestRoute, DistMatr)  # считаем длину начального маршрута
    # print(SP)
    for i in AllRoutes:  # перебираем все маршруты и ищем кратчайший
        CurrDist = CountRoute(i, DistMatr)
        if CurrDist < BestRouteDist:
            BestRouteDist = CurrDist
            BestRoute = i
    print()
    print("Best route is", BestRoute, " Best distance =", BestRouteDist)
    return DistMatr, BestRoute, BestRouteDist

def MatrixToTxt(Matrix,file):#функция вывода в файл матрицы расстояний через табуляцию
    for i in range(len(Matrix)):
        for j in range(len(Matrix[i])):
            file.write(str(Matrix[i][j])+"\t")
        # file.write("\b")
        file.write("\n")
    return
# ______________________________________________________________________________________________
#создадим папку для сохранения пар матрица-оптимальный маршрут
CurrDir = os.getcwd()
# print(CurrDir)
if not os.path.isdir("Result"):
     os.mkdir("Result")
os.chdir("Result")
CurrDir = os.getcwd()
# print(CurrDir)

N = 20 #задаем N
for i in range(5):#создаем 5 txt файлов с матрицей, опт маршрутом и расстоянием
    filename = CurrDir+"\\"+str(i)+".txt"
    if os.path.isfile(filename):
        os.remove(filename)
    # print(filename)
    f =open(filename,'w')
# ______________________________________________________________________________________________
    DistMatr,BestRoute,BRDistance = FullTaskSolver(N,10,90) #решаем задачу полным перебором
    MatrixToTxt(DistMatr,f)
    f.write(str(BestRoute)+"\n")
    f.write(str(BRDistance))
    # f.write(str(i))
    # f.write(str(i+1))
    f.close()



