import numpy as np
import json
import math

# M, N 的 值
M = 4
N = 4
# 每个位置可交换的位置集合
pos = np.arange(M*N).reshape(M, N)
g_dict_shifts = {}
for i in range(0, M):
    for j in range(0, N):
        a = []
        if i-1 >= 0:
            a.append(pos[i-1][j])
        if i+1 < M:
            a.append(pos[i+1][j])
        if j-1 >= 0:
            a.append(pos[i][j-1])
        if j+1 < N:
            a.append(pos[i][j+1])
        g_dict_shifts[pos[i][j]] = a


g_dict_layouts = {}
g_dict_layouts_deep = {}
g_dict_layouts_fn = {}


def swap_chr(a, i, j, deep, destLayout):
    if i > j:
        i, j = j, i
    # 得到ij交换后的数组
    b = a[:i] + a[j] + a[i+1:j] + a[i] + a[j+1:]
    # 存储fn,A*算法
    fn = cal_dislocation_sum(b, destLayout)+deep
    return b, fn


# 返回错码和正确码距离之和
def cal_dislocation_sum(srcLayout, destLayout):
    sum = 0
    a = srcLayout.index("0")
    for i in range(0, M*N):
        pos = destLayout.index(srcLayout[i])
        if i != a:
            srcx = math.ceil((i+1)/N)
            destx = math.ceil((pos+1)/N)
            srcy = math.ceil((i+1) % N)
            desty = math.ceil((pos+1) % N)
            sum = sum + abs(srcx-destx) + abs(srcy-desty)
    return sum


def solvePuzzle_A(srcLayout, destLayout):
    # 先进行判断srcLayout和destLayout的逆序值,在M×N的问题中，空格的行距离同样影响求解
    src = 0
    dest = 0
    for i in range(1, M*N):
        fist = 0
        for j in range(0, i):
            if srcLayout[j] > srcLayout[i] and srcLayout[i] != '0':
                fist = fist+1
        src = src + fist
    for i in range(1, M*N):
        fist = 0
        for j in range(0, i):
            if destLayout[j] > destLayout[i] and destLayout[i] != '0':
                fist = fist+1
        dest = dest + fist
    for z in range(0, M*N):
        if srcLayout[z] == '0':
            srcspace = math.ceil((z+1)/N)
        if destLayout[z] == '0':
            destspace = math.ceil((z+1)/N)
    dis = abs(destspace - srcspace)
    # 分N的奇偶性讨论
    # N为奇数时，和八数码问题判定一致
    if N % 2 == 1:
        # 奇偶性不同，目标状态不可达
        if (src % 2) != (dest % 2):
            return -1, None
    # N为偶数时：
    if N % 2 == 0:
        # 奇偶性相同，但空格距离为奇数，目标状态不可达
        if (src % 2) == (dest % 2) and dis % 2 == 1:
            return -1, None
        # 奇偶性不同，但空格距离为偶数，目标状态不可达
        if (src % 2) != (dest % 2) and dis % 2 == 0:
            return -1, None

    g_dict_layouts[srcLayout] = -1
    g_dict_layouts_deep[srcLayout] = 1
    g_dict_layouts_fn[srcLayout] = 1 + cal_dislocation_sum(srcLayout, destLayout)
    stack_layouts = []
    # 深度值
    gn = 0
    # 当前状态存入列表
    stack_layouts.append(srcLayout)
    count = 0
    while len(stack_layouts) > 0:
        count = count + 1
        curLayout = min(g_dict_layouts_fn, key=g_dict_layouts_fn.get)
        del g_dict_layouts_fn[curLayout]
        # 找到最小fn，并移除
        stack_layouts.remove(curLayout)
        # curLayout = stack_layouts.pop()
        # 判断当前状态是否为目标状态
        if curLayout == destLayout:
            break
        # 寻找0 的位置。
        ind_slide = curLayout.index("0")
        # 当前可进行交换的位置集合
        lst_shifts = g_dict_shifts[ind_slide]
        for nShift in lst_shifts:
            newLayout, fn = swap_chr(curLayout, nShift, ind_slide, g_dict_layouts_deep[curLayout] + 1, destLayout)
            # 判断交换后的状态是否已经查询过
            if g_dict_layouts.get(newLayout) == None:
                # 存入深度
                g_dict_layouts_deep[newLayout] = g_dict_layouts_deep[curLayout] + 1
                # 存入fn
                g_dict_layouts_fn[newLayout] = fn
                # 定义前驱结点
                g_dict_layouts[newLayout] = curLayout
                # 存入集合
                stack_layouts.append(newLayout)
    lst_steps = []
    lst_steps.append(curLayout)
    # 存入路径
    while g_dict_layouts[curLayout] != -1:
        curLayout = g_dict_layouts[curLayout]
        lst_steps.append(curLayout)
    lst_steps.reverse()
    print('Search Step:', count, 'step')
    return 0, lst_steps


if __name__ == "__main__":
    # 测试数据
    srcLayout = "1234056789ABCDEF"
    destLayout = "8574136290DBCEAF"

    retCode, lst_steps = solvePuzzle_A(srcLayout, destLayout)
    if retCode != 0:
        print("目标布局不可达")
    else:
        for nIndex in range(len(lst_steps)):
            print("step #" + str(nIndex + 1))
            for i in range(0, M):
                print(lst_steps[nIndex][i*N:i*N+N])
    result = {'m': M, 'n': N, 'k': 1, 'data': lst_steps}
    file_name = str(M) + '×' + str(N) + '.json'  # 通过扩展名指定文件存储的数据为json格式
    with open(file_name, 'w') as file_object:
        json.dump(result, file_object)
