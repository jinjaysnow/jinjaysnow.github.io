Title:  Git相关
Authors: Jin Jay
Date:    2014-10
Description: Git相关问题：创建仓库、创建分支、合并分支、删除分支等等。
keywords: git
          github


# 创建一个仓库

    git init

# 分支
## 创建一个分支

    git checkout -b newbranch
相当于

    git branch newbranch
    git checkout newbranch
`git checkout`作用是切换到某一个分支。比如想切换回master分支可以使用`git checkout master`.

## 合并分支

    git checkout master
    git merge newbranch
Git自动合并，但没有提交，它会停下来等你解决冲突。要看看哪些文件在合并时发生冲突，可以用`git status`查阅。  
任何包含未解决冲突的文件都会以未合并（unmerged）的状态列出。Git会在有冲突的文件里加入标准的冲突解决标记，可以通过它们来手工定位并解决这些冲突。  
`git mergetool`可以使用图形化的合并工具。再使用`git status`查看冲突状态。
## 删除分支

    git branch -d newbranch 












[TOC]
