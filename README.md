
## 开发前准备
*注意：开发同学必读章节*

### 环境配置
本项目使用uv替代pip安装依赖，uv是一个快速的Python包管理器，安装速度快。
同时，本项目配置了pre-commit，用于在提交代码前进行代码格式化和检查。
在正式开始开发前，请先按照如下命令执行，安装uv和pre-commit，以及项目依赖。
```bash
sh scripts/setup_dev_env.sh
```
#### 依赖管理
本项目所有依赖均在 `pyproject.toml` 文件中进行管理，可通过如下命令进行安装/移除
```bash
uv add <package-name>
uv remove <package-name>
```
#### 代码检查
本项目使用pre-commit进行代码检查和格式化，配置文件位于 `.pre-commit-config.yaml`。
在每次提交代码前，pre-commit会自动运行检查和格式化。如果检查不通过，提交会被拒绝。
可以通过如下命令手动运行pre-commit检查：
```bash
pre-commit run --all-files
```
如果需要紧急跳过pre-commit检查，可在提交命令后添加 `--no-verify` 参数，例如：
```bash
git commit -m "feat: add new feature" --no-verify
```
### 日志管理
本项目使用loguru进行日志管理，日志配置位于 `src/core/logging.py`。
#### 日志级别
默认日志级别为INFO，可通过环境变量 `LOG_LEVEL` 进行覆盖。
例如，在开发环境中可以设置为DEBUG，以便查看更详细的日志信息。
```bash
export LOG_LEVEL=DEBUG
```
#### 日志文件
日志文件默认保存在 `logs` 目录下，按日期进行分割。
可以通过环境变量 `LOG_FILE_PATH` 进行覆盖。
例如：
```bash
export LOG_FILE_PATH=/app/logs
```

### 配置项
本项目所有配置项均可通过环境变量进行覆盖。
#### 新增配置项
如需新增配置项，在 `src/config` 文件中增加相应的配置字段，并赋予默认值。如果是数据库URL等不适合在代码写死默认配置，可以在.env文件中配置开发环境默认值。
#### 使用配置项
z在代码中使用配置项时，直接从 `config` 模块导入即可。例如：
```python
from src.config import Config

project_name = Config.PROJECT_NAME
```
#### 配置项说明
在服务部署阶段，可以通过环境变量覆盖默认配置。例如，在Docker Compose中可以这样配置：
```yaml
services:
  app:
    environment:
      - PROJECT_NAME=My Awesome App
```
在docker启动命令中也可以配置环境变量，例如：
```bash
docker run -e PROJECT_NAME=My Awesome App -p 8000:8000 my-awesome-app
```
在k8s中也可以配置环境变量，例如：
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-awesome-app
spec:
  containers:
    - name: app
      image: my-awesome-app
      env:
        - name: PROJECT_NAME
          value: My Awesome App
```

## 服务部署
### 镜像构建
在项目根目录下执行如下命令构建Docker镜像：

```bash
sh scripts/build_docker.sh
# 或者指定标签和Dockerfile路径
sh scripts/build_docker.sh -t v1.0.0 -f docker/Dockerfile
```
### 服务启动
构建完成后，可以通过如下命令启动服务：
```bash
sh scripts/run_docker.sh
# 或者自定义配置
sh scripts/run_docker.sh -t v1.0.0 -n fastapi-demo-container-local -p 8000 -w 1
```
### 本地调试
在本地调试时，可通过如下命令启动服务：
```bash
sh scripts/run_docker_local.sh
```

## 接口文档
服务启动后，有如下3种方式查看接口文档：
1. 访问 `http://localhost:8000/api/v1/docs` 查看自动生成的Swagger接口文档。
2. 访问 `http://localhost:8000/api/v1/redoc` 查看自动生成的ReDoc接口文档。
3. 访问 `http://localhost:8000/api/v1/openapi.json` 查看OpenAPI规范的JSON文档。
