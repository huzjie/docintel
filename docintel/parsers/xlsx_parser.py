# -*- coding: utf-8 -*-
"""XLSX 解析器（zip + XML，纯 stdlib）。"""
from __future__ import annotations

import io
import re
import zipfile
import xml.etree.ElementTree as ET

from ..types import Document, Table, TableCell
from .base import BaseParser

_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def _col_to_idx(col: str) -> int:
    n = 0
    for c in col:
        n = n * 26 + (ord(c.upper()) - ord("A") + 1)
    return n - 1


class XlsxParser(BaseParser):
    extensions = ["xlsx", "xlsm"]
    mime_types = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
    binary = True

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        doc = self._new_doc(source, "xlsx")
        zf = zipfile.ZipFile(io.BytesIO(data))
        # 工作表名
        sheet_names = _sheet_names(zf)
        doc.title = sheet_names[0] if sheet_names else source
        all_text = []
        # 共享字符串
        shared = _shared_strings(zf)
        for sn in sheet_names:
            try:
                sheet_xml = zf.read(f"xl/worksheets/{sn}.xml") if _sheet_file_exists(zf, sn) else None
            except KeyError:
                sheet_xml = None
            if sheet_xml is None:
                # 尝试读 workbook 里的 r:id 映射（简化：直接枚举）
                for cand in _candidate_sheet_files(zf):
                    sheet_xml = zf.read(cand)
                    break
            if sheet_xml is None:
                continue
            table = _parse_sheet(sheet_xml, shared)
            all_text.append(_table_to_text(table))
            doc.tables.append(Table(id=f"t{len(doc.tables)}", rows=table.rows,
                                    caption=sn, header_rows=1))
        doc.text = "\n\n".join(all_text)
        return doc


def _sheet_names(zf):
    try:
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        names = []
        for s in wb.iter(f"{{{_NS}}}sheet"):
            if "name" in s.attrib:
                names.append(s.attrib["name"])
        return names
    except Exception:
        return []


def _sheet_file_exists(zf, name):
    try:
        zf.getinfo(f"xl/worksheets/{name}.xml")
        return True
    except KeyError:
        return False


def _candidate_sheet_files(zf):
    return sorted([n for n in zf.namelist()
                   if re.match(r"xl/worksheets/sheet\d+\.xml", n)])


def _shared_strings(zf):
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        out = []
        for si in root.iter(f"{{{_NS}}}si"):
            txt = "".join(t.text or "" for t in si.iter(f"{{{_NS}}}t"))
            out.append(txt)
        return out
    except KeyError:
        return []


def _parse_sheet(sheet_xml: bytes, shared):
    root = ET.fromstring(sheet_xml)
    from ..types import Table
    table = Table(id="tmp")
    max_col = 0
    for row in root.iter(f"{{{_NS}}}row"):
        cells = {}
        for c in row.iter(f"{{{_NS}}}c"):
            ref = c.attrib.get("r", "")
            m = re.match(r"([A-Z]+)(\d+)", ref)
            col = _col_to_idx(m.group(1)) if m else 0
            cell_type = c.attrib.get("t", "")
            v = c.find(f"{{{_NS}}}v")
            if cell_type == "s" and v is not None:
                try:
                    val = shared[int(v.text)]
                except (ValueError, IndexError):
                    val = v.text or ""
            else:
                val = v.text if v is not None else ""
            # 内联字符串
            if not val:
                is_t = c.find(f"{{{_NS}}}is")
                if is_t is not None:
                    val = "".join(t.text or "" for t in is_t.iter(f"{{{_NS}}}t"))
            cells[col] = val
            max_col = max(max_col, col)
        if cells:
            row_cells = [TableCell(text=str(cells.get(i, ""))) for i in range(max_col + 1)]
            table.rows.append(row_cells)
    return table


def _table_to_text(table):
    return "\n".join("\t".join(c.text for c in row) for row in table.rows)


__all__ = ["XlsxParser"]
