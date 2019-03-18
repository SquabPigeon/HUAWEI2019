class RoadInfo(object):
    def __init__(self,name = 5000, filename_road = 'data/test2/testRoad.txt'):
        self.m_roadName = name
        self.m_filename = filename_road

    def readFile(self):
        with open(self.m_filename,'r') as f:
            listLines = f.readlines();#将所有信息读到list中
            paraList = []
            SingleList=[]
            TotalList = []
            for i in range(0,len(listLines)):
                listLines[i] = listLines[i].rstrip('\n')#去掉换行符以及左右括号
                listLines[i] = listLines[i].strip("()")
                #list[i] = list[i].strip(")")
                line = listLines[i].split(",")#以逗号为分界划分成片
                if line[0] == "#(id":
                    a=1
                else:
                    for j in range(0,len(line)):
                        SingleList.append(line[j])
                    #SingleList = list(map(int,SingleList))
                    TotalList.append(SingleList)
                    SingleList=[]
            for i in range(0, len(TotalList)):
                TotalList[i] = list(map(int, TotalList[i]))
        return TotalList
    #返回对应编号道路的信息
    def road_data(self):
        TotalRoadData_List = self.readFile()
        for TotalRoadData_List_i in TotalRoadData_List:
            if self.m_roadName == TotalRoadData_List_i[0]:
                return TotalRoadData_List_i
        return []




class TrafficInfo(object):
    def __init__(self, filename = 'data/test2/testCross.txt'):
        self.m_filename = filename
        #self.m_crossNum = []
        #self.m_crossNet = {}
        self.m_crossNum = []
        self.m_crossNet = {}

    #读文件
    def readFile(self):
        with open(self.m_filename,'r') as f:
            listLines = f.readlines();#将所有信息读到list中
            paraList = []
            SingleList=[]
            TotalList = []
            for i in range(0,len(listLines)):
                listLines[i] = listLines[i].rstrip('\n')#去掉换行符以及左右括号
                listLines[i] = listLines[i].strip("()")
                #list[i] = list[i].strip(")")
                line = listLines[i].split(",")#以逗号为分界划分成片
                if line[0] == "#(id":
                    a=1
                else:
                    for j in range(0,len(line)):
                        SingleList.append(line[j])
                    #SingleList = list(map(int,SingleList))
                    TotalList.append(SingleList)
                    SingleList=[]
            for i in range(0, len(TotalList)):
                TotalList[i] = list(map(int, TotalList[i]))
            self.m_crossNum = TotalList
        return TotalList
    #读文件
    def readFile2(self,m_filename):
        with open(m_filename,'r') as f:
            listLines = f.readlines();#将所有信息读到list中
            paraList = []
            SingleList=[]
            TotalList = []
            for i in range(0,len(listLines)):
                listLines[i] = listLines[i].rstrip('\n')#去掉换行符以及左右括号
                listLines[i] = listLines[i].strip("()")
                #list[i] = list[i].strip(")")
                line = listLines[i].split(",")#以逗号为分界划分成片
                if line[0] == "#(id":
                    a=1
                else:
                    for j in range(0,len(line)):
                        SingleList.append(line[j])
                    #SingleList = list(map(int,SingleList))
                    TotalList.append(SingleList)
                    SingleList=[]
            for i in range(0, len(TotalList)):
                TotalList[i] = list(map(int, TotalList[i]))
            #self.m_crossNum = TotalList
        return TotalList


    #找到单个节点的所有邻接节点，并输出成字典
    def SingleNode(self, iList,TotalList):
        result_dictionary = {}
        single_data = TotalList[iList]
        for i in range(1,len(single_data)):
            if single_data[i] != -1:
                for j in range(0, len(TotalList)):
                    if j!=iList and  TotalList[j].count(single_data[i])>0:
                        single_road = RoadInfo(single_data[i])
                        result_dictionary[TotalList[j][0]] = single_road
                        break
        return result_dictionary
    #将读出文件的信息整理成一个嵌套字典
    def TotalNode(self):
        result_dictionary = {}
        single_dictionary ={}
        TotalList = self.readFile()
        for i in range(0,len(TotalList)):
            single_dictionary = self.SingleNode(i,TotalList)
            result_dictionary[TotalList[i][0]] = single_dictionary
            single_dictionary = []
        self.m_crossNet = result_dictionary
        return result_dictionary

    #根据road.txt中最后一位的信息去除不可逆道路
    def RemoveIrreversibleRoads(self, m_filename_road):
        '''

        :param m_crossNet:
        :param m_filename_road:
        :return:
        '''
        m_roadMSG = self.readFile2(m_filename_road)
        for Road_SingleLine in m_roadMSG:
            if Road_SingleLine[-1] != 1:
                self.m_crossNet[Road_SingleLine[-2]].pop(Road_SingleLine[-3])



    def shortestPath_(self,cross1,cross2,is_traversedInfo):
        '''
        :param cross1:
        :param cross2:
        :param is_traversedInfo:
        :return:节点列表，最短路径
        '''
        is_traversedInfo[cross1] = True
        temp_answer = []
        for next_key,next_value in m_crossNet[cross1].items():
            #到达终点
            if next_key == cross2:
                road_msg = m_crossNet[cross1][next_key].road_data()
                return [road_msg[0]],road_msg[1]
            if is_traversedInfo[next_key]:
                return [],0
            temp_tup = self.shortestPath_(next_key, cross2, is_traversedInfo)
            temp_list = [m_crossNet[cross1][next_key].road_data()[0]] + temp_tup[0]
            temp_length = m_crossNet[cross1][next_key].road_data()[1] + temp_tup[1]
            temp_tup_next = (temp_list,temp_length)
            temp_answer.append(temp_tup_next)
            #temp_answer[next_key] = self.shortestPath_(next_key, cross2, is_traversedInfo)
        #temp_list = temp_answer.items()
        # 按路线长度进行排序
        temp_answer.sort(key=lambda x: x[1])
        right_way = temp_answer[0]
        #return [m_crossNet[cross1][next_key].road_data()[0]] + right_way[0], m_crossNet[cross1][next_key].road_data()[1] + right_way[1]
        return right_way[0], right_way[1]

    # 返回最短路径，如果不可达则返回空数组
    def shortestPath(self,start_cross,end_cross):
        '''

        :param start_cross:
        :param end_cross:
        :return: 节点列表，最短长度
        '''
        cross_Data = self.readFile()#得到一个cross信息list
        # is_traversedInfo 用于标志是否访问过
        is_traversedInfo = {cross_Data[i][0]:False for i in range(len(cross_Data))}
        return self.shortestPath_(start_cross,end_cross,is_traversedInfo)


RI1 = RoadInfo()
m_roadData = RI1.readFile()
Tr1 = TrafficInfo()
m_crossNum = Tr1.readFile()
m_crossNet = Tr1.TotalNode()
Tr1.RemoveIrreversibleRoads('data/test2/testRoad.txt')
#for next_key,next_value in m_crossNet[1].items():
a,b = Tr1.shortestPath(1,7)
print(a,b)
pass



