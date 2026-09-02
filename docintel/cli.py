# -*- coding: utf-8 -*-
"""docintel 命令行入口。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .config import load_config
from .core.pipeline import Pipeline


def _cmd_parse(args):
    cfg = load_config(args.config)
    pipe = Pipeline(cfg)
    result = pipe.run_file(args.input)
    doc = result.document
    if args.json:
        from .output.renderer import render as r
        print(r(doc, "json"))
    else:
        from .output.renderer import render as r
        print(r(doc, args.format))
    if args.verbose:
        print("\n--- pipeline ---", file=sys.stderr)
        for line in result.pipeline_log:
            print("  " + line, file=sys.stderr)
        print(f"elapsed={result.elapsed_ms}ms", file=sys.stderr)
    return 0


def _cmd_formats(_args):
    from .parsers.registry import list_parsers
    print("支持的输入格式:", ", ".join(list_parsers()))
    print("支持的输出格式: markdown, json, html, csv")
    return 0


def _cmd_doctor(_args):
    from .parsers.registry import list_parsers
    from .providers.base import list_providers
    cfg = load_config(_args.config)
    print(f"docintel {__version__}")
    print(f"provider      : {cfg.get('provider', 'mock')}")
    print(f"parsers       : {', '.join(list_parsers())}")
    print(f"providers     : {', '.join(list_providers())}")
    print("status        : OK")
    return 0


def _cmd_serve(args):
    from .config import load_config
    cfg = load_config(args.config)
    # 优先 FastAPI，缺依赖回退 stdlib
    try:
        import uvicorn  # noqa: F401
        from .api import create_app
        app = create_app(cfg)
        import uvicorn as uv
        uv.run(app, host=cfg.get("server", {}).get("host", "127.0.0.1"),
               port=cfg.get("server", {}).get("port", 8000))
    except ImportError:
        from .server_stdlib import run_server
        run_server(cfg)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="docintel", description="智能文档解析与结构化抽取平台")
    p.add_argument("--config", default="config.json", help="配置文件路径")
    p.add_argument("--version", action="store_true", help="显示版本")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("parse", help="解析文档")
    sp.add_argument("input", help="输入文件路径")
    sp.add_argument("-f", "--format", default="markdown", help="输出格式")
    sp.add_argument("--json", action="store_true", help="输出 JSON")
    sp.add_argument("-v", "--verbose", action="store_true", help="打印管道日志")
    sp.set_defaults(func=_cmd_parse)

    sf = sub.add_parser("formats", help="列出支持的格式")
    sf.set_defaults(func=_cmd_formats)

    sd = sub.add_parser("doctor", help="环境自检")
    sd.set_defaults(func=_cmd_doctor)

    ss = sub.add_parser("serve", help="启动 HTTP 服务")
    ss.set_defaults(func=_cmd_serve)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
