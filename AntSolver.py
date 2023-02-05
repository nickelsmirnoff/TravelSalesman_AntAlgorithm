import os
import random as rnd
import numpy as np

def FileParser(FileName):#функция парсинга входного файла. возвращает матрицу расстояний, строку лучшего маршрута, оптимальное расстояние
    f = open(FileName, "r")
    AllStrings = f.readlines()
    BRDistance = int(AllStrings[len(AllStrings)-1])#получаем оптимальное расстояние как последнюю строку в файле
    AllStrings.pop(len(AllStrings)-1)#удаляем последнюю строку
    BestRoute = AllStrings[len(AllStrings)-1]#получаем оптимальный маршрут как последнюю строку файла
    BestRoute = BestRoute.replace("\n","")
    AllStrings.pop(len(AllStrings) - 1)  #удаляем последнюю строку
    Matrix = []
    for str in AllStrings:#заполняем матрицу Matrix построчно числами из строк файла
        StringArray = str.split("\t")
        StringArray.pop(len(StringArray)-1)#удаляем последний символ \n
        TempString = []
        for num in StringArray:
            TempString.append(int(num))
        Matrix.append(TempString)
    return Matrix, BestRoute, BRDistance

def StartFeromoneMatrix(D):
    N = len(D)
    #создадим начальную матрицу феромонов, в начале по каждой строке суммарное значение 1
    Fer = []
    for i in range(N):
        CurrString = D[i]
        CurrFerr = []
        Sum = sum(CurrString)
        for j in range(N):
            CurrFerr.append(D[i][j]/ Sum)
        Fer.append(CurrFerr)
        # print(CurrFerr)
        # print (sum(CurrFerr))
    return Fer

def MatrixReverse(D,beta): #функция расчета матрицы (1/Dij)**beta
    N = len(D)
    Rev = []
    for i in range(N):
        NewString = []
        for j in range(N):
            if D[i][j] == 0:
                NewString.append(0)
                continue
            NewString.append((1/D[i][j])**beta)
        Rev.append(NewString)
        # print(NewString)
    return Rev

def NextCityChoice(Ant,P,D):  #функция выбора муравьем следующего города для вектора вероятностей P
    if not Ant.AvailableCities:
        print ("No available cities")
        return
    Range = list(range(len(P)))
    # print(Range)
    NextCity = rnd.choices(Range, weights = P)
    Ant.AddCity(NextCity[0], D)
    # if not Ant.AvailableCities:
    #     print(Ant.__dict__)
    # NextCity = rnd.choices(Range, weights=[0,0,0,0.8,0.2])
    # print(NextCity)
    return

def KmatrixFiller(Ants,K): # функция заполнения матрицы К номерами муравьев, прошедших i-j маршрутом
    for i in range(len(Ants)):
        CurRoute = Ants[i].CurRoute
        for j in range(len(CurRoute)-1):
            K[CurRoute[j]][CurRoute[j+1]].add(i)

def FeromoneUpdate(Ferr, Ants, K, ro, Q): # функция обновления феромона
    for i in range(len(Ferr)):
        for j in range(len(Ferr)):
            Sum = 0
            if not K[i][j]:
                Ferr[i][j] = Ferr[i][j] * (1 - ro)
                continue
            for k in K[i][j]:
                # print(K[i][j],k)
                Sum+= Ants[k].CurDist
            # print(Sum)
            Ferr[i][j] = Ferr[i][j]*(1-ro)+Q/Sum
    return

def MinFromArr(Arr):
    N = len(Arr)
    Numbers = []
    for i in range(N):
        Numbers.append(Arr[i][0])
    min = np.min(Numbers)
    minroute = Arr[np.argmin(Numbers)][1]
    # print(min)
    # print(minroute)
    return min, minroute

def FerrRouteBuilder(Ferr,D): # функция построения оптимального маршрута на основании матрицы феромонов
    Solves = []
    for t in range(len(D)):
        Ant1 = Ant(t,D)
        # print(Ant1.__dict__)
        for i in range(len(D)-1):
            arr = Ferr[Ant1.CurCity].copy()
            while Ant1.AvailableCities:
                # arr.pop(0)
                m = np.argmax(arr)
                if not m in Ant1.AvailableCities:
                    arr[m] = 0
                    continue
                Ant1.AddCity(m,D)
        # Solves[str(Ant1.CurDist)]= str(Ant1.CurRoute)
        vect = [Ant1.CurDist, Ant1.CurRoute]
        Solves.append(vect)
        # print(Ant1.CurRoute,"<-",Ant1.CurDist)
        # print(Ant1.__dict__)
    # best = np.min()
    # print(Solves)
    min, route = MinFromArr(Solves)
    print(route,"<-",min)
    # bestD = np.min(Solves.keys())
    # bestR = Solves[str(BestD)]
    # print(bestD,bestR)
    return

def AntAlgorithmSolver(D, alpha, beta, Q, ro, AntNumber, IterNumber):
    # функция принимает на вход матрицу расстояний D, альфа, бета, Q, ро, количество муравьев и количество итераций
    Ferr = StartFeromoneMatrix(D)  # создаем начальную матрицу распределения феромона
    D1 = MatrixReverse(D, beta)  # создаем матрицу обратных расстояний 1/dij в степени бета
    # print(D1)
    # Ant1 = Ant(1,D)
    # print(Ant1.__dict__)
    # Ant1.AddCity(4, D)
    # print(Ant1.__dict__)
    # Ant1.AddCity(2, D)
    # print(Ant1.__dict__)
    # Ant1.AddCity(3, D)
    # print(Ant1.__dict__)
    # Ant1.AddCity(2, D)
    # Ant2 = Ant(3,D)
    # print(Ant2.__dict__)
    # Ant2.AddCity(4,D)
    # print(Ant2.__dict__)
    # создаем экземпляры класса Ant в количестве AntNumber и сохраняем в список Ants
    for step in range(IterNumber):
        Ants = []
        for i in range(AntNumber): # случайная расстановка муравьев по городам с повторениями
            newAnt = Ant(rnd.randint(0, len(D) - 1), D)
            Ants.append(newAnt)
        # for i in range(AntNumber):
            # Ants[i].AddCity(rnd.randint(0, len(D) - 1), D)
            # print(f"Ants[{i}]: {Ants[i].__dict__}")
            # print(Ants[i].ProbCalculator(Ferr, alpha, D1))
        # Ants[0].AddCity(0,D)
        # Ants[0].AddCity(1,D)
        # print(f"Ants[0]: {Ants[0].__dict__}")
        # print(Ants[0].ProbCalculator(Ferr, alpha, D1))
        # Ants[0].AddCity(2,D)
        # print(f"Ants[0]: {Ants[0].__dict__}")
        # print(Ants[0].ProbCalculator(Ferr, alpha, D1))
        # Ants[0].AddCity(3,D)
        # print(f"Ants[0]: {Ants[0].__dict__}")
        # print(Ants[0].ProbCalculator(Ferr, alpha, D1))
        # Ants[0].AddCity(4,D)
        # print(f"Ants[0]: {Ants[0].__dict__}")
        # print(Ants[0].ProbCalculator(Ferr, alpha, D1))
        K = [[set() for j in range(len(D))] for i in range(len(D))]# K - матрица номеров муравьев, выбравших i-j маршрут. Заполняем пуст множ
        for ant_i in Ants: # один пробег всех муравьев по замкнутому маршруту
            for j in range(len(D)-1): # пока не кончится список доступных городов
                NextCityChoice(ant_i,ant_i.ProbCalculator(Ferr,alpha,D1),D) # случайный выбор следующего города по Р
            # print()
        KmatrixFiller(Ants,K)# заполняем матрицу K
        # for i in Ferr:
        #     print(i)
        FeromoneUpdate(Ferr, Ants, K,ro,Q)# обновляем феромон данной функцией
        # print()
        # for i in Ferr:
        #     print(i)
        for i in range(AntNumber):
            del Ants[0]
        # print(Ants)
    # for fer in Ferr:
    #     print(np.round(fer,decimals=2))
    # print()
    FerrRouteBuilder(Ferr,D)


    return

class Ant:
    "класс муравей со всей информацией по нему: CurCity, AvailableCities, CurRoute, CurDist"
    def __init__(self,CurCity,D): # конструктор класса, получает параметр ТекГород и матрицу расстояний,
        # создает список доступн городов, считает ТекМаршрут и ТекРасстояние
        self.CurCity = CurCity
        self.CurRoute = []
        self.CurRoute.append(self.CurCity)
        self.CurDist = 0
        self.AvailableCities = set(range(len(D)))
        self.AvailableCities.discard(CurCity)

    def CurrentDistance(self,D):
        if len(self.CurRoute) == 1:
            return 0
        else:
            for i in range(len(self.CurRoute) -1):
                self.CurDist += D[self.CurRoute[i]][self.CurRoute[i+1]]
            return self.CurDist

    def AddCity(self,City,D):#функция перехода муравья в город City
        if City >= len(D):
            print(f"Cannot add city number {City} because we have only {len(D)} cities")
            return
        if City in self.CurRoute:
            print(f"Cannot add city number {City} because it is visited: {self.CurRoute}")
            return

        self.CurDist += D[self.CurRoute[-1]][City]
        self.CurRoute.append(City)
        self.AvailableCities.discard(City)
        self.CurCity = City
        # для последнего города - автоматически дописываем возвращение в начальный город
        if not self.AvailableCities:
            LastCity = self.CurRoute[0]
            self.CurDist += D[City][LastCity]
            self.CurRoute.append(LastCity)
            self.CurCity = LastCity
        return

    def ProbCalculator(self, Ferr, alpha, D1):  # функция вычисления вероятностей перехода в города для одного муравья
        if not self.AvailableCities:
            print("No available cities")
            return 0 # возвращает 0 при отсутствии доступных городов
        ProbString = [0 for i in range(len(D1))]
        StringSum = 0
        for i in self.AvailableCities:
            StringSum+= (Ferr[self.CurCity][i]**alpha) * D1[self.CurCity][i]
        for i in range(len(D1)):
            if i not in self.AvailableCities:
                ProbString[i] = 0
            else:
                ProbString[i] = (Ferr[self.CurCity][i]**alpha) * D1[self.CurCity][i] / StringSum
        return ProbString # возвращает вектор вероятностей

#______________________________________________________________________________________________________________________
if not os.path.isdir("Input"): #если папки нет - пишем сообщение и выходим из скрипта
    #print("Current Directory is",os.getcwd())
    print("Directory \"Input\" not found in current directory")
    raise SystemExit()
else:
    os.chdir("Input")
CurrDir = os.getcwd()
FilesList = os.listdir(CurrDir)
for FileName in FilesList: #проходим по всем входным файлам и вытаскиваем из них данные
    if os.path.isdir(FileName):
        #print(FileName+" is directory")
        continue
    print("__________________________________________________________________")
    print(FileName)
    Matrix,Route,Distance = FileParser(FileName)#получаем матрицу расстояний, лучший маршрут и оптимальное расстояние
    for i in range(len(Matrix)):
        print(Matrix[i])
    print()
    print(Route," <-",Distance)
    print("Processing")


    #запускаем функцию решения задачи муравьиным алгоритмом для полученных данных
    # AntAlgorithmSolver(Matrix, 1, 0, 50, 0.1, 5, 50000)# парамерты D,alpha,beta,Q,ro,AntNumber,IterNumber
    # AntAlgorithmSolver(Matrix, 0, 1, 50, 0.1, 5, 50000)  # парамерты D,alpha,beta,Q,ro,AntNumber,IterNumber
    AntAlgorithmSolver(Matrix, 0.5, 0.5, 25, 0.1, 50, 10)  # парамерты D,alpha,beta,Q,ro,AntNumber,IterNumber
    AntAlgorithmSolver(Matrix, 0.5, 0.5, 10, 0.1, 50, 100)
    AntAlgorithmSolver(Matrix, 0.5, 0.5, 5, 0.1, 50, 1000)
    AntAlgorithmSolver(Matrix, 0.5, 0.5, 1, 0.1, 50, 10000)


