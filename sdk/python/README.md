# docintel Python SDK

```python
from docintel_sdk import Docintel

client = Docintel("config.json")
result = client.parse_file("合同.pdf")
print(client.to_markdown(result))
print(result.document.summary())
```
