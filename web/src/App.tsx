import React, { useCallback, useState } from "react";

interface Summary {
  source: string; format: string; title: string; pages: number;
  blocks: number; tables: number; images: number; chunks: number; fields: number;
}

export default function App() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [markdown, setMarkdown] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onDrop = useCallback(async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    const file = files[0];
    setLoading(true);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      const resp = await fetch("/parse?fmt=markdown", { method: "POST", body: form });
      const data = await resp.json();
      setSummary(data.summary);
      setMarkdown(data.markdown || "");
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="container">
      <header>
        <h1>docintel</h1>
        <p>智能文档解析与结构化抽取平台</p>
      </header>

      <div
        className="dropzone"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); onDrop(e.dataTransfer.files); }}
      >
        <input
          type="file"
          onChange={(e) => onDrop(e.target.files)}
          style={{ display: "none" }}
          id="file"
        />
        <label htmlFor="file">拖拽文档到这里，或点击选择文件</label>
        <span className="hint">支持 PDF / Word / Excel / PPT / HTML / 图片 / 文本</span>
      </div>

      {loading && <p className="status">解析中…</p>}
      {error && <p className="error">{error}</p>}

      {summary && (
        <div className="result">
          <h2>解析结果</h2>
          <div className="grid">
            <Metric label="标题" value={summary.title || "—"} />
            <Metric label="格式" value={summary.format} />
            <Metric label="页数" value={String(summary.pages)} />
            <Metric label="块" value={String(summary.blocks)} />
            <Metric label="表格" value={String(summary.tables)} />
            <Metric label="图片" value={String(summary.images)} />
            <Metric label="分块" value={String(summary.chunks)} />
            <Metric label="字段" value={String(summary.fields)} />
          </div>
          {markdown && <pre className="markdown">{markdown.slice(0, 6000)}</pre>}
        </div>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span className="label">{label}</span>
      <span className="value">{value}</span>
    </div>
  );
}
