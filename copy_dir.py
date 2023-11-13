'''
function:
    copy a src dir to dst with files you wanted,and delete empty dirs copyed in dst
    you can copy .dll file like this:
        python copy_dir path/to/dll_dir path/to/dst_dir  .*\.dll
    or header files like this:
        python copy_dir path/to/src path/to/dst .*\.h .*\.hpp
    have fun!
python version when coding: 3.9.13
platform: intel x8664 windows
author: vo17245
'''
import pathlib
import os
import re
import sys
def PrintUsage():
    print("Usage: python copy_dir <src> <dst> <pattern>...")
def CopyFile(src,dst):
    file_src=open(src,"rb")
    file_dst=open(dst,"wb")
    buf_size=1024
    buf=file_src.read(buf_size)
    while len(buf)!=0:
        file_dst.write(buf)
        buf=file_src.read(buf_size)
    file_src.close()
    file_dst.close()
def main():
    argv=sys.argv
    if len(argv)<3:
        PrintUsage()
        exit(-1)
    
    src=pathlib.Path(argv[1])
    dst=pathlib.Path(argv[2])
    dst_dirs_exist_before_copy=[]
    for root,dirs,files in os.walk(dst):
        dst_dirs_exist_before_copy.append(root)
    patterns=[]
    for i in range(len(argv)-3):
        patterns.append(argv[3+i])
    for root,dirs,files in os.walk(src):
        path_root=pathlib.Path(root)
        for dir in dirs:
            path_dir=pathlib.Path(dir)
            path_dir=path_root/path_dir
            relative_path_dir=path_dir.relative_to(src)
            path_dir_dst=dst/relative_path_dir
            if not os.path.exists(path_dir_dst):
                
                os.makedirs(path_dir_dst)
        for file in files:
            path_file=pathlib.Path(file)
            path_file=path_root/path_file
            relative_path_file_dst=path_file.relative_to(src)
            path_file_dst=dst/relative_path_file_dst
            if os.path.exists(path_file_dst):
                continue
            flag=0
            for pattern in patterns:
                name=""
                try:
                    name=path_file.name
                except Exception:
                    pass
                
                if name=="":
                    name=path_file
                
                if re.match(pattern,name)!=None:
                    flag=1
                    break
            if flag==1:
                CopyFile(path_file,path_file_dst)
    dirs_to_del=[]
    for root,dirs,files in os.walk(dst):
        if len(dirs)==0 and len(files)==0:
            dirs_to_del.append(root)
    
    while len(dirs_to_del)!=0:
        for dir in dirs_to_del:
            if dir not in dst_dirs_exist_before_copy:
                os.rmdir(dir)
        dirs_to_del=[]
        for root,dirs,files in os.walk(dst):
            if len(dirs)==0 and len(files)==0:
                dirs_to_del.append(root)
        
if __name__=="__main__":
    main()