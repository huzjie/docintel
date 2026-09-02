# docintel API 参考

## Python 核心 API

### `Pipeline(config: dict)`

| 方法 | 说明 |
|------|------|
| `run(data, source, ext) -> ParseResult` | 跑完整流水线 |
| `run_file(path) -> ParseResult` | 解析文件 |
| `to_output(result, fmt) -> str` | 渲染输出 |

### `load_file(path) -> Document`

直接加载并解析单个文件（不走 chunk/extract 阶段）。

## HTTP API

`POST /parse?fmt=json`，multipart 表单字段 `file`。

响应（fmt=json）：
```json
{
  "summary": { "source": "合同.pdf", "format": "pdf", "pages": 3, "tables": 1 },
  "data": { "title": "...", "text": "...", "blocks": [], "tables": [], "chunks": [] }
}
```

响应（fmt=markdown）：
```json
{ "summary": {}, "markdown": "# 合同\n..." }
```

## 抽取 schema 字段

| schema | 字段 |
|--------|------|
| invoice | 发票号码、开票日期、销售方名称、购买方名称、金额合计、税额 |
| contract | 合同名称、甲方、乙方、签署日期、合同金额、生效日期、到期日期 |
| resume | 姓名、学历、工作年限、技能、最近公司 |
