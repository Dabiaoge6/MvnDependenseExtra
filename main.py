import subprocess
import re
import sys

import pandas as pd

# 指定Maven项目的目录
# project_directory = r"D:\work\sca\靶场\mall-1.0.0\mall-1.0.0"
# command = "mvn dependency:tree -Dverbose"
# 运行mvn dependency:tree命令并获取输出
def run_maven_tree(workdir,cmd):
    process = subprocess.Popen(cmd, cwd=workdir, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    return output

# 解析Maven依赖树输出


# def parse_dependenciesByFile():
#     dependencies = []
#     first=[]
#     twice=[]
#     third=[]
#     forth=[]
#     fifth=[]
#     with open('maventreeERP', 'r', encoding='utf-8') as file:
#         # 逐行读取文件内容
#         for line in file:
#             line = line.strip()
#             if ":jar:" in line and "[INFO]" in line:
#                 line = line[7:] # remove [INFO]
#                 level = line.count("|")
#                 # print(line)
#                 name = line.split("-", 1)[1].strip() # the part after the -
#                 if "omitted for duplicate)" in name :
#                     continue
#                 if " " in name:
#                     name = name.split(" ")[0]
#                     status = "judge"
#                 else:
#                     status = "use"
#
#                 print("level = ",level ,"gav = ",name ,"status = ",status)
#                 if level == 0:
#                     first.append({
#                         "name":name,
#                         "status":status
#                     })
#                 if level == 1:
#                     twice.append({
#                         "name": name,
#                         "status": status
#                     })
#                 if level == 2:
#                     third.append({
#                         "name": name,
#                         "status": status
#                     })
#                 if level == 3:
#                     forth.append({
#                         "name": name,
#                         "status": status
#                     })
#                 if level == 4:
#                     fifth.append({
#                         "name": name,
#                         "status": status
#                     })
#                 # dependencies.append(name)
#     dependencies = excuteDependencies(first,twice,third,forth,fifth)
#     dependencies = cleanDependencies(dependencies)
#     dependencies = list(set(dependencies))
#     return dependencies

def parse_dependencies(output):
    dependencies = []
    first=[]
    twice=[]
    third=[]
    forth=[]
    fifth=[]
    lines = output.strip().split('\n')
        # 逐行读取文件内容
    for line in lines:
        line = line.strip()
        if ":jar:" in line and "[INFO]" in line:
            line = line[7:] # remove [INFO]
            level = line.count("|")
            # print(line)
            name = line.split("-", 1)[1].strip() # the part after the -
            if "omitted for duplicate)" in name :
                continue
            if " " in name:
                name = name.split(" ")[0]
                status = "judge"
            else:
                status = "use"

            print("level = ",level ,"gav = ",name ,"status = ",status)
            if level == 0:
                first.append({
                    "name":name,
                    "status":status
                })
            if level == 1:
                twice.append({
                    "name": name,
                    "status": status
                })
            if level == 2:
                third.append({
                    "name": name,
                    "status": status
                })
            if level == 3:
                forth.append({
                    "name": name,
                    "status": status
                })
            if level == 4:
                fifth.append({
                    "name": name,
                    "status": status
                })
            # dependencies.append(name)
    dependencies = excuteDependencies(first,twice,third,forth,fifth)
    dependencies = cleanDependencies(dependencies)
    dependencies = list(set(dependencies))
    return dependencies
def excuteDependencies(first,twice,third,forth,fifth):
    dependencies = []

    for i in first:
        dependencies.append(i["name"])
    for i in twice:
        if i["status"] == "use":
            dependencies.append(i["name"])
        else:
            exit = str(dependencies)
            dependencies = judgeExit(i,dependencies)
    for i in third:
        if i["status"] == "use":
            dependencies.append(i["name"])
        else:
            exit = str(dependencies)
            dependencies = judgeExit(i,dependencies)
    for i in forth:
        if i["status"] == "use":
            dependencies.append(i["name"])
        else:
            exit = str(dependencies)
            dependencies = judgeExit(i,dependencies)
    for i in fifth:
        if i["status"] == "use":
            dependencies.append(i["name"])
        else:
            dependencies = judgeExit(i,dependencies)
    return dependencies

def cleanDependencies(dependencies):
    print("=====clean============")
    result = []
    for i in dependencies:
        ## 取出scop 并删除"jar"
        var = i.split(":")[0:-1]
        var.remove("jar")
        i = ":".join(var)

        ##删掉结果中的(
        if "(" in i:
            i = i[1:]
        result.append(i)
    return result

def judgeExit(dependency , dependencies):
    print(dependency["name"])

    if "(" in dependency["name"]:
        dependency["name"] = dependency["name"][1:]

    if str(dependency["name"]).split("jar")[0] not in str(dependencies):
        dependencies.append(dependency["name"])
    print("排除",dependency["name"])
    return dependencies


# 保存依赖信息到Excel
def save_to_excel(dependencies, file_name='dependencies.xlsx'):
    df = pd.DataFrame(dependencies, columns=['Dependency'])
    df.to_excel(file_name, index=False)


# 解析命令行参数
def parse_arguments():
    args = sys.argv[1:]  # 忽略脚本名称
    workdir = None
    cmd = None
    save = None
    for arg in args:
        if arg.startswith('--workdir'):
            workdir = arg.split('=')[1]
            continue
        if arg.startswith('--cmd'):
            cmd = arg.split('=')[1]
            continue
        if arg.startswith('--save'):
            save = arg.split('=')[1]
            continue
    print("cmd=",cmd)
    print("workdir=",workdir)
    print("save=",save)
    return workdir, cmd,save
def main():
    workdir ,cmd ,save =parse_arguments()
    output = run_maven_tree(workdir,cmd)
    dependencies = parse_dependencies(output)
    print("保存表格")
    save_to_excel(dependencies, file_name='save.xlsx')

if __name__ == "__main__":
    main()