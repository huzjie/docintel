# docintel 部署指南

## Docker

```bash
docker build -t docintel .
docker run -d -p 8000:8000 -v $PWD/data:/app/.docintel docintel
```

## Kubernetes

```bash
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/configmap.yaml
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
```

## Helm

```bash
helm install docintel deploy/helm/docintel
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `DOCINTEL_PROVIDER` | 默认 LLM provider |
| `DOCINTEL_PROVIDERS__<NAME>__API_KEY` | 各 provider 密钥 |
| `DOCINTEL_PIPELINE__ENABLE_EXTRACT` | 开启 LLM 抽取 |
| `DOCINTEL_SERVER__PORT` | 服务端口 |
