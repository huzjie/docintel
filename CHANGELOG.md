# Changelog

## [1.0.0] - 2026-08-30

### Added
- 多格式解析：PDF / DOCX / XLSX / PPTX / HTML / Markdown / TXT / CSV / JSON / XML / 邮件 / 图片
- 版面分析：标题 / 段落 / 列表 / 代码块分类（中文标题 + 数字编号启发式）
- 表格抽取：有边框网格表 + 无边框流式表启发式聚类
- OCR：tesseract 引擎 + mock 兜底
- PII 脱敏：手机号 / 身份证 / 邮箱 / 银行卡
- 语义分块：fixed / sliding / structure / semantic
- LLM 结构化抽取：发票 / 合同 / 简历 schema，容错 JSON 解析
- 多 Provider：OpenAI 兼容 / Anthropic / DeepSeek / Qwen / Ollama / mock
- 结构化输出：Markdown / JSON / HTML / CSV / TXT
- FastAPI 控制面 + stdlib 兜底 + CLI + Python/TS SDK + React 控制台
- Docker / K8s / Helm / CI / CodeQL
