# docintel · 智能文档解析与结构化抽取平台

> 把 **PDF / Word / Excel / PPT / HTML / 图片 / 邮件 / CSV** 等非结构化文档，
> 一键转成 **AI-ready 的结构化数据**（Markdown / JSON / 表格 / 语义字段），
> 供 RAG、知识库、大模型应用直接消费。

<p align="center">
  <img src="https://img.shields.io/badge/license-Apache--2.0-blue" alt="license" />
  <img src="https://img.shields.io/badge/python-3.9%2B-green" alt="python" />
  <img src="https://img.shields.io/badge/deps-zero--runtime-orange" alt="zero deps" />
  <img src="https://img.shields.io/badge/status-stable-brightgreen" alt="status" />
</p>

---

## 目录

- [为什么需要 docintel](#为什么需要-docintel)
- [核心能力](#核心能力)
- [架构](#架构)
- [快速开始](#快速开始)
- [配置](#配置)
- [命令行 CLI](#命令行-cli)
- [HTTP API](#http-api)
- [Python SDK](#python-sdk)
- [TypeScript SDK](#typescript-sdk)
- [Web 控制台](#web-控制台)
- [结构化抽取（LLM）](#结构化抽取llm)
- [部署](#部署)
- [项目结构](#项目结构)
- [测试](#测试)
- [License](#license)

---

## 为什么需要 docintel

大模型落地最痛的环节不是「模型」，而是「数据」。企业的合同、发票、简历、报表、
知识库文档散落在 PDF / Word / 扫描件里，结构混乱、无法被 RAG 或 Agent 直接检索。

docintel 对标 **Cohere Parse 5** 等文档解析能力，提供一条**开箱即用、可自托管、
内核零依赖**的文档 → 结构化数据流水线：

```
非结构化文档 ──▶ 解析 ─▶ 版面分析 ─▶ 表格抽取 ─▶ OCR ─▶ PII脱敏 ─▶ 语义分块 ─▶ [LLM字段抽取] ─▶ 结构化输出
```

## 核心能力

| 能力 | 说明 |
|------|------|
| **多格式解析** | PDF / DOCX / XLSX / PPTX / HTML / Markdown / TXT / CSV / JSON / 图片，共 20+ 扩展名 |
| **版面分析** | 标题 / 段落 / 列表 / 代码块自动分类（中文「第X章」、数字编号、列表符启发式） |
| **表格抽取** | 有边框网格表（`|`、制表符）+ 无边框流式表启发式聚类，转 `Table` 结构化对象 |
| **OCR** | 扫描件 / 图片文字识别，tesseract 引擎 + mock 兜底，纯 stdlib 图像预处理 |
| **PII 脱敏** | 手机号 / 身份证 / 邮箱 / 银行卡正则脱敏，可配置占位符 |
| **语义分块** | fixed / sliding / structure / semantic 四种策略，供 RAG 使用 |
| **LLM 结构化抽取** | 发票 / 合同 / 简历内置 schema，容错 JSON 解析，多 Provider |
| **结构化输出** | Markdown / JSON / HTML / CSV 四种渲染 |
| **多 Provider** | OpenAI 兼容 / Anthropic / DeepSeek / Qwen / Ollama / mock |

## 架构

```
                        ┌─────────────────────────────────────────┐
                        │              HTTP 控制面                │
                        │  FastAPI (/parse /formats /tasks)        │
                        │  + stdlib server 兜底 (无依赖可跑)        │
                        └──────────────────┬──────────────────────┘
                                           │
                        ┌──────────────────▼──────────────────────┐
                        │               Pipeline                  │
                        │  parse → layout → table → ocr → redact   │
                        │        → chunk → [extract] → output     │
                        └───────┬──────────┬──────────┬───────────┘
                                │          │          │
                    ┌───────────▼──┐ ┌─────▼────┐ ┌───▼─────────┐
                    │   parsers    │ │  layout  │ │ extract     │
                    │ pdf/docx/    │ │  tables  │ │ chunk/ocr   │
                    │ xlsx/pptx/   │ │          │ │ output      │
                    │ html/image/  │ └──────────┘ └─────────────┘
                    │ text/csv/json│
                    └──────────────┘
                                │
                    ┌───────────▼──────────────────────────────┐
                    │  providers   storage   security   metrics │
                    │  (LLM 适配)  (SQLite)  (脱敏/限额) (Prom) │
                    └──────────────────────────────────────────┘
```

**设计原则**：内核（解析/版面/表格/分块/输出/脱敏）**纯标准库零依赖**，
离线即可跑通 mock 端到端；PDF 完整解析、OCR、FastAPI 均为**惰性可选增强**。

## 快速开始

### 零依赖（最快）

```bash
# 1. 克隆
git clone https://github.com/<you>/docintel.git && cd docintel

# 2. 直接跑（无需 pip install，纯标准库）
python -m docintel.cli doctor
python -m docintel.cli parse examples/sample.txt
```

### 完整模式

```bash
pip install -e .
pip install -r requirements.txt   # fastapi / pypdf / pytesseract 等可选增强

docintel serve                    # 启动 HTTP 服务（http://127.0.0.1:8000）
```

### 解析一份合同

```bash
docintel parse 合同.pdf -f markdown     # 输出 Markdown
docintel parse 合同.pdf --json          # 输出 JSON
docintel parse 合同.pdf -v              # 打印管道日志
```

## 配置

配置三层：内置默认 → `config.json` → `DOCINTEL_*` 环境变量（`__` 表示层级）。

```bash
# 复制示例配置
cp config.example.json config.json

# 用环境变量覆盖（无需改文件）
export DOCINTEL_PROVIDER=deepseek
export DOCINTEL_PROVIDERS__DEEPSEEK__API_KEY=sk-xxx
export DOCINTEL_PIPELINE__ENABLE_EXTRACT=true
export DOCINTEL_PIPELINE__EXTRACT_SCHEMA=contract
```

## 命令行 CLI

```bash
docintel doctor          # 环境自检
docintel formats         # 列出支持格式
docintel parse <file>    # 解析文档
docintel serve           # 启动 HTTP 服务
```

## HTTP API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET  | `/healthz` | 健康检查 |
| GET  | `/formats` | 支持的输入/输出格式 |
| POST | `/parse?fmt=json\|markdown` | 上传文件解析（multipart `file`） |
| GET  | `/tasks` | 任务历史 |

```bash
curl -F "file=@合同.pdf" "http://127.0.0.1:8000/parse?fmt=json"
```

## Python SDK

```python
from docintel_sdk import Docintel

client = Docintel("config.json")
result = client.parse_file("合同.pdf")
print(client.to_markdown(result))
print(result.document.summary())
```

## TypeScript SDK

```ts
import { DocintelClient } from "docintel-sdk";

const client = new DocintelClient("http://127.0.0.1:8000");
const res = await client.parseFile(file, "json");
console.log(res.summary);
```

## Web 控制台

```bash
cd web && npm install && npm run dev   # 拖拽文档即时解析
```

## 结构化抽取（LLM）

```json
// config.json
{
  "provider": "deepseek",
  "providers": { "deepseek": { "api_key": "sk-xxx", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat" } },
  "pipeline": { "enable_extract": true, "extract_schema": "contract" }
}
```

内置 schema：`invoice`（发票）、`contract`（合同）、`resume`（简历）。
无 API Key 时 `provider=mock` 离线也能跑通端到端。

## 部署

```bash
# Docker
docker build -t docintel .
docker run -p 8000:8000 docintel

# docker-compose
docker compose up -d

# Kubernetes
kubectl apply -f deploy/k8s/

# Helm
helm install docintel deploy/helm/docintel
```

## 项目结构

```
docintel/
├── docintel/            # 核心 Python 包（纯标准库）
│   ├── core/            # Pipeline + loader
│   ├── parsers/         # 9 类解析器 + 注册表
│   ├── layout/          # 版面分析
│   ├── tables/          # 表格抽取
│   ├── ocr/             # OCR 引擎
│   ├── extract/         # LLM 结构化抽取 + schema
│   ├── chunk/           # 语义分块
│   ├── output/          # Markdown/JSON/HTML/CSV 渲染
│   ├── providers/       # LLM Provider 适配器
│   ├── storage/         # SQLite 存储
│   ├── security/        # PII 脱敏 + 限额
│   ├── observability/   # 指标 + 追踪
│   ├── cli.py           # 命令行
│   ├── api.py           # FastAPI
│   └── server_stdlib.py # 无依赖 HTTP 兜底
├── sdk/                 # Python + TypeScript SDK
├── web/                 # React 深色控制台
├── tests/               # 测试
├── deploy/              # K8s / Helm
├── docs/                # 文档
├── examples/            # 示例文档
└── .github/             # CI / CodeQL / dependabot
```

## 测试

```bash
pip install pytest
pytest tests/ -q
```

## License

[Apache-2.0](LICENSE)
