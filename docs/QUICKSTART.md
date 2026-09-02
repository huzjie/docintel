# docintel 快速上手

## 1. 安装

```bash
git clone https://github.com/<you>/docintel.git
cd docintel
pip install -e .
```

## 2. 验证

```bash
docintel doctor
```

## 3. 解析文档

```bash
docintel parse examples/sample.txt
docintel parse 合同.pdf --json
```

## 4. 启动服务

```bash
docintel serve
# 访问 http://127.0.0.1:8000/docs
```

## 5. 接入 LLM 抽取

编辑 `config.json` 填入 API Key，开启 `enable_extract`。
