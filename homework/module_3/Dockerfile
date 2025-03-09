# 第一阶段：构建阶段 (使用更小的 Alpine 镜像)
FROM golang:1.24-alpine AS builder

# 设置容器内工作目录
WORKDIR /app

# 复制所有源代码到容器
COPY . .

# 构建静态二进制文件（禁用 CGO，减少依赖）
RUN CGO_ENABLED=0 GOOS=linux go build -o tcp-server -ldflags="-w -s" tcp_server.go

# 第二阶段：运行阶段 (使用最小化镜像)
FROM alpine:3.19

# 从构建阶段复制编译好的二进制文件
COPY --from=builder --chown=appuser:appgroup /app/tcp-server /app/tcp-server

# 暴露 TCP 端口
EXPOSE 3333

# 启动应用程序
CMD ["/app/tcp-server"]