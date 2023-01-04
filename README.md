常用工具
===========
## runJs
原理：拷贝选中内容至指定配置文件，默认为{user}/tmp.js，利用sublime自带build进行执行，因此需要设定sublime的build必要配置。

配置build
```
Tools -> Build System -> New Build System
```
填写如下信息，source.js写死就可以，命名随意，如：JavaScript.sublime-build
```
{  
    "cmd": ["/usr/local/bin/node", "/Users/fengzhikui/tmp/tmp.js"],  
    "selector": "source.js"  
}
```

## timeformat
快捷键: 选中文本 ctrl + e
格式化时间支持 
````
yyyy-MM-dd HH:mm:ss
yyyy-MM-dd
0000000000
0000000000000
````

## clear_panel
快捷键: ctrl + L
