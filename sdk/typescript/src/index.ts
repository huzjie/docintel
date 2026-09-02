/**
 * docintel TypeScript SDK — 调用 docintel HTTP 服务。
 */

export interface ParseSummary {
  source: string;
  format: string;
  title: string;
  pages: number;
  blocks: number;
  tables: number;
  images: number;
  chunks: number;
  fields: number;
  word_count: number;
}

export interface ParseResponse {
  summary: ParseSummary;
  data?: Record<string, unknown>;
  markdown?: string;
}

export class DocintelClient {
  private baseUrl: string;

  constructor(baseUrl = "http://127.0.0.1:8000") {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  async healthz(): Promise<{ status: string; version: string }> {
    return this.request<{ status: string; version: string }>("/healthz");
  }

  async parseFile(file: File | Blob, format: "json" | "markdown" = "json"): Promise<ParseResponse> {
    const form = new FormData();
    form.append("file", file);
    const url = `${this.baseUrl}/parse?fmt=${format}`;
    const resp = await fetch(url, { method: "POST", body: form });
    if (!resp.ok) {
      const err = await resp.text();
      throw new Error(`docintel parse failed: ${resp.status} ${err}`);
    }
    return resp.json();
  }

  private async request<T>(path: string): Promise<T> {
    const resp = await fetch(this.baseUrl + path);
    if (!resp.ok) throw new Error(`docintel request failed: ${resp.status}`);
    return resp.json();
  }
}

export default DocintelClient;
