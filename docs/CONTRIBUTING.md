# 贡献指南

## 开发环境

```bash
git clone <repo>
pip install -e .
pip install -r requirements.txt
pip install pytest
```

## 运行测试

```bash
pytest tests/ -q
python -m compileall docintel
```

## 代码风格

- 内核（docintel/ 包）纯标准库零依赖
- 可选增强（pypdf / pytesseract / fastapi）惰性导入
- 新增解析器继承 `BaseParser` 并在 `registry._build_registry` 注册
- 新增测试放 `tests/test_*.py`
