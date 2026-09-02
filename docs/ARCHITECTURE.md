# docintel 架构设计

## 设计目标

1. **内核零依赖**：解析 / 版面 / 表格 / 分块 / 输出 / 脱敏 全部纯标准库，离线可跑。
2. **可选增强**：PDF 完整解析、OCR、FastAPI、React 控制台均为惰性导入。
3. **一条流水线**：`Pipeline.run(bytes) -> ParseResult` 单一入口，各阶段可开关。

## 数据流

```
bytes ─▶ load_bytes ─▶ Document
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
   LayoutAnalyzer   TableExtractor      OcrEngine (仅图片)
        │                 │                  │
        └────────┬────────┘                  │
                 ▼                            │
           PiiRedactor ◀──────────────────────┘
                 │
                 ▼
            Chunker ─▶ Chunk[]
                 │
                 ▼
        LlmExtractor (可选) ─▶ ExtractedField[]
                 │
                 ▼
          render(doc, fmt) ─▶ str
```

## 核心模型（types.py）

- `Document`：解析结果根对象（text/blocks/tables/images/chunks/fields）
- `Block`：版面块（type + level）
- `Table` / `TableCell`：结构化表格
- `Chunk`：RAG 分块
- `ExtractedField`：LLM 抽取字段

## 扩展点

- **新增解析器**：继承 `BaseParser`，设置 `extensions`，在 `registry._build_registry` 注册。
- **新增 Provider**：继承 `BaseProvider`（OpenAI 兼容），或自定义 `complete`。
- **新增抽取 schema**：在 `extract/schema.py` 增加 `classmethod`。
- **新增分块策略**：在 `chunk/strategies.py` 增加类并注册到 `_STRATEGIES`。
