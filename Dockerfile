# 使用官方的 Python 基础镜像
# 选择一个与你开发环境一致的特定版本
FROM python:3.11-slim

# 设置环境变量，防止 Python 写入 .pyc 文件并配置路径
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 安装构建 mysqlclient 所需的系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        pkg-config \
        default-libmysqlclient-dev \
        build-essential \
        gcc && \
    rm -rf /var/lib/apt/lists/*

# 更新 pip
RUN pip install --upgrade pip

# 复制依赖文件并安装
# 这一步单独做可以利用 Docker 的层缓存，如果 requirements.txt 没有变化，则不会重新安装
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制所有项目代码到工作目录
COPY . .

# 运行 collectstatic 命令来收集所有静态文件
RUN python manage.py collectstatic --noinput

# 暴露容器的 8000 端口，以便外部可以访问
EXPOSE 8000

# 容器启动时运行的命令
# 使用 gunicorn 启动 Django 应用
CMD ["gunicorn", "DigiOverTime.wsgi:application", "--bind", "0.0.0.0:8000"]