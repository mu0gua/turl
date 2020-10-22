# turl.exe


```
# 基于HTTP的非动态交互请求伪造。

> turl.exe 
  __               .__
_/  |_ __ _________|  |
\   __\  |  \_  __ \  |
 |  | |  |  /|  | \/  |__
 |__| |____/ |__|  |____/
                           by: mugua

Usage of turl.exe:
  -l    show module list
  -m string
        use module name (support regx)
  -q string
        query data (support @file @dir)
```

- - -

# Example:

```
# step1: create file: example.json
[
    {
        "name": "example",
        "desc": "example",
        "method": "GET",
        "url": "https://www.baidu.com/?q=`content`",
        "header": {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        },
        "data": "`content`",
        "response_regx": ""
    }
]

# step2: config.yaml set example.json path

plugin: ./plugin/

# step3: turl -m example (support regx) -q test (support @file @dir)

# step4: waiting program run.

```


# other

```
# auto parse file.
python turl_parse.py 
```

