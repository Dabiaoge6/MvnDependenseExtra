## 用途
自动提取maven构建时用到的组件，并会在提取过程中采取就近原则处理存在“版本冲突”的组件，组件提取完毕后将依赖的组件保存至excel表中
## 使用方法
```python .\main.py --workdir="D:\work\sca\靶场\mall-1.0.0\mall-1.0.0" --cmd="mvn dependency:tree -Dverbose" --save="./test3.xlsx"```

参数解释：
- workdir 待编译项目路径
- cmd 执行的maven解析依赖树命令
- save 组件保存路径
