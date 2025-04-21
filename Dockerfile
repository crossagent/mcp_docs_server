# 基础镜像（仍然用官方的瘦身版）
FROM python:3-slim

# ---------- 端口 ----------
EXPOSE 33286

# ---------- 运行期环境变量 ----------
ENV PYTHONDONTWRITEBYTECODE=1        

# ---------- 安装 uv ----------
# 1) 先升级 pip（防止旧版依赖解析慢）
# 2) 安装 uv ── 这是 Astral 家基于 Rust 的包管理器/执行器
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir uv

# ---------- 安装项目依赖 ----------
# 复制依赖定义文件
COPY pyproject.toml uv.lock* ./ 
# 使用 uv sync 从 lock 文件安装精确依赖
RUN uv sync

# ---------- 拷贝源码并设置工作目录 ----------
WORKDIR /app
COPY . /app

# ---------- 创建非 root 用户 ----------
RUN adduser -u 5678 --disabled-password --gecos "" appuser \
    && chown -R appuser /app
USER appuser

# ---------- 容器启动命令 ----------
# 这里用 uv 执行 server.py 脚本，由脚本内部启动 uvicorn
CMD ["uv", "run", "python", "server.py"]
