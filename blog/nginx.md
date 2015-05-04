Title:   Nginx
Author: JinJay 靳杰
Date:    2015-04
description: Nginx配置与使用
keywords: Nginx


# 测试配置是否正确
`nginx -t`

# 反向代理配置
```
# 配置工作的进程数
worker_processes  4;

# 连接数
events {
    worker_connections 1024;
    # use epoll; 根据系统配置是否使用epoll
}

# 反向代理配置
http {
    # 分发
    upstream tornadoes {
        #服务器配置： 权重越大，分配概率越大
        server 127.0.0.1:8881 weight=1;
        server 127.0.0.1:8882 weight=1;
        server 127.0.0.1:8883 weight=1;
        server 127.0.0.1:8884 weight=1;
    }

    server {
        listen 8888;
        server_name localhost;
        location / {
            proxy_pass http://tornadoes;
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
        }
    }
}
```

[TOC]