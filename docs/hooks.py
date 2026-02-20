from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MethodDoc:
    name: str
    params: list[tuple[str, str | None]]
    http_method: str | None
    api_path: str | None
    response_type: str | None


@dataclass
class EndpointDoc:
    class_name: str
    client_path: str
    methods: list[MethodDoc]


@dataclass
class ModelField:
    name: str
    annotation: str | None


def _snake_words(text: str) -> list[str]:
    clean = re.sub(r"Endpoint$", "", text)
    pieces = re.findall(r"[A-Z]+(?=[A-Z][a-z]|\b)|[A-Z]?[a-z]+|\d+", clean)
    words: list[str] = []
    for piece in pieces:
        token = piece.lower()
        if token.isdigit() and words:
            words[-1] = f"{words[-1]}{token}"
            continue
        words.append(token)
    return words


def _longest_common_prefix(a: list[str], b: list[str]) -> int:
    size = 0
    for left, right in zip(a, b):
        if left != right:
            break
        size += 1
    return size


def _longest_common_suffix(a: list[str], b: list[str]) -> int:
    size = 0
    for left, right in zip(reversed(a), reversed(b)):
        if left != right:
            break
        size += 1
    return size


def _attr_segment(parent_words: list[str], child_words: list[str]) -> str:
    if not child_words:
        return ""

    prefix = _longest_common_prefix(parent_words, child_words)
    suffix = _longest_common_suffix(parent_words, child_words)
    prefix_trimmed = child_words[prefix:] if prefix else child_words[:]
    suffix_trimmed = child_words[: len(child_words) - suffix] if suffix else child_words[:]

    candidates = [c for c in (prefix_trimmed, suffix_trimmed) if c]
    if not candidates:
        return "_".join(child_words)

    best = min(candidates, key=len)
    return "_".join(best)


def _collect_http_call(node: ast.FunctionDef) -> tuple[str | None, str | None]:
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
            if child.func.attr in {"_get", "_post"} and child.args:
                first = child.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    verb = "GET" if child.func.attr == "_get" else "POST"
                    return verb, first.value
    return None, None


def _response_from_annotation(node: ast.FunctionDef) -> str | None:
    if node.returns is None:
        return None
    if isinstance(node.returns, ast.Constant) and isinstance(node.returns.value, str):
        return node.returns.value
    try:
        return ast.unparse(node.returns)
    except Exception:
        return None


def _response_from_apiresponse_model_validate(node: ast.FunctionDef) -> str | None:
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        if not isinstance(child.func, ast.Attribute):
            continue
        if child.func.attr != "model_validate":
            continue
        owner = child.func.value
        if not isinstance(owner, ast.Subscript):
            continue
        if not isinstance(owner.value, ast.Name):
            continue
        if owner.value.id != "ApiResponse":
            continue
        try:
            return ast.unparse(owner.slice)
        except Exception:
            return None
    return None


def _response_from_post_call(node: ast.FunctionDef) -> str | None:
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        if not isinstance(child.func, ast.Attribute):
            continue
        if child.func.attr != "_post" or len(child.args) < 2:
            continue
        try:
            model_name = ast.unparse(child.args[1])
        except Exception:
            return None
        return model_name
    return None


def _normalize_type_name(type_name: str | None) -> str | None:
    if not type_name:
        return None
    normalized = type_name.replace("self.", "")
    normalized = normalized.replace("typing.", "")
    normalized = re.sub(r"\s+", "", normalized)
    if normalized.startswith("ApiResponse[") and normalized.endswith("]"):
        normalized = normalized[len("ApiResponse[") : -1]
    return normalized or None


def _collect_response_type(node: ast.FunctionDef) -> str | None:
    annotation = _normalize_type_name(_response_from_annotation(node))
    if annotation:
        return annotation

    model_validate = _normalize_type_name(_response_from_apiresponse_model_validate(node))
    if model_validate:
        return model_validate

    from_post = _normalize_type_name(_response_from_post_call(node))
    if from_post:
        return from_post

    return None


def _annotation_text(node: ast.arg) -> str | None:
    if node.annotation is None:
        return None
    try:
        return ast.unparse(node.annotation)
    except Exception:
        return None


def _example_value(name: str, annotation: str | None) -> str:
    lower_name = name.lower()
    ann = (annotation or "").lower()

    if "bool" in ann or lower_name.startswith(("is_", "has_")):
        return "False"
    if "int" in ann or any(key in lower_name for key in ("count", "port", "id")):
        return "1"
    if "float" in ann:
        return "1.0"
    return f'"{name}_value"'


def _method_call(method: MethodDoc) -> str:
    if not method.params:
        return f"{method.name}()"

    args = [f"{name}={_example_value(name, ann)}" for name, ann in method.params]
    return f"{method.name}({', '.join(args)})"


def _annotation_from_expr(expr: ast.expr) -> str | None:
    try:
        return ast.unparse(expr)
    except Exception:
        return None


def _is_basemodel_subclass(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id == "BaseModel":
            return True
        if isinstance(base, ast.Attribute) and base.attr == "BaseModel":
            return True
    return False


def _collect_model_schemas(module_ast: ast.Module) -> dict[str, list[ModelField]]:
    models: dict[str, list[ModelField]] = {}

    def walk(node: ast.ClassDef) -> None:
        if _is_basemodel_subclass(node):
            fields: list[ModelField] = []
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    fields.append(
                        ModelField(
                            name=item.target.id,
                            annotation=_annotation_from_expr(item.annotation),
                        )
                    )
            models[node.name] = fields

        for item in node.body:
            if isinstance(item, ast.ClassDef):
                walk(item)

    for item in module_ast.body:
        if isinstance(item, ast.ClassDef):
            walk(item)

    return models


def _split_top_level_union(type_name: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    start = 0
    for index, char in enumerate(type_name):
        if char == "[":
            depth += 1
        elif char == "]":
            depth = max(depth - 1, 0)
        elif char == "|" and depth == 0:
            parts.append(type_name[start:index])
            start = index + 1
    parts.append(type_name[start:])
    return [part for part in parts if part]


def _strip_optional(type_name: str) -> str:
    stripped = type_name.strip()
    if stripped.startswith("Optional[") and stripped.endswith("]"):
        return stripped[len("Optional[") : -1]
    if stripped.startswith("None|"):
        return stripped[len("None|") :]
    if stripped.endswith("|None"):
        return stripped[: -len("|None")]
    return stripped


def _collect_return_fields(
    type_name: str,
    models: dict[str, list[ModelField]],
    prefix: str = "data",
    depth: int = 0,
) -> list[tuple[str, str]]:
    if depth > 4:
        return [(prefix, "Any")]

    current = _strip_optional(type_name)
    if not current:
        return [(prefix, "Any")]

    unions = [u.strip() for u in _split_top_level_union(current)]
    if len(unions) > 1:
        union_label = " | ".join(unions)
        return [(prefix, union_label)]

    current = unions[0]
    if current.startswith("list[") and current.endswith("]"):
        inner = current[5:-1]
        return _collect_return_fields(inner, models, f"{prefix}[]", depth + 1)
    if current.startswith("List[") and current.endswith("]"):
        inner = current[5:-1]
        return _collect_return_fields(inner, models, f"{prefix}[]", depth + 1)
    if current.startswith("Dict[") or current.startswith("dict["):
        return [(prefix, current)]
    if current in {"str", "int", "float", "bool"}:
        return [(prefix, current)]
    if current in models:
        fields: list[tuple[str, str]] = []
        for field in models[current]:
            field_type = field.annotation or "Any"
            fields.extend(
                _collect_return_fields(
                    field_type,
                    models,
                    f"{prefix}.{field.name}",
                    depth + 1,
                )
            )
        return fields or [(prefix, current)]

    return [(prefix, current)]


def _example_scalar(annotation: str) -> object:
    lower = annotation.lower()
    if "bool" in lower or lower in {"literal[0,1]", "literal['0','1']", 'literal["0","1"]'}:
        return "__TYPE_bool__"
    if lower in {"int", "integer"}:
        return "__TYPE_int__"
    if lower in {"float"}:
        return "__TYPE_float__"
    return "__TYPE_string__"


def _example_data_for_type(
    type_name: str,
    models: dict[str, list[ModelField]],
    depth: int = 0,
) -> object:
    if depth > 3:
        return "__TYPE_any__"

    if not type_name:
        return None

    raw = _strip_optional(type_name)
    options = [opt.strip() for opt in _split_top_level_union(raw)]
    chosen = options[0] if options else raw.strip()

    if chosen.startswith("list[") and chosen.endswith("]"):
        inner = chosen[5:-1]
        return [_example_data_for_type(inner, models, depth + 1)]
    if chosen.startswith("List[") and chosen.endswith("]"):
        inner = chosen[5:-1]
        return [_example_data_for_type(inner, models, depth + 1)]
    if chosen.startswith("Dict[") or chosen.startswith("dict["):
        return {}
    if chosen in {"str", "int", "float", "bool"}:
        return _example_scalar(chosen)
    if chosen in models:
        payload: dict[str, object] = {}
        for field in models[chosen]:
            payload[field.name] = _example_data_for_type(
                field.annotation or "str", models, depth + 1
            )
        return payload

    return "__TYPE_any__"


def _render_response_json(method: MethodDoc, models: dict[str, list[ModelField]]) -> str:
    data_example = _example_data_for_type(method.response_type or "Any", models)
    payload = {
        "success": True,
        "data": data_example,
        "errors": None,
    }
    rendered = json.dumps(payload, indent=2)
    replacements = {
        '"__TYPE_string__"': "string",
        '"__TYPE_int__"': "int",
        '"__TYPE_float__"': "float",
        '"__TYPE_bool__"': "bool",
        '"__TYPE_any__"': "any",
    }
    for source, target in replacements.items():
        rendered = rendered.replace(source, target)
    return rendered


def _parse_endpoint_class(
    node: ast.ClassDef,
    parent_words: list[str],
    parent_path: str,
    is_root: bool = False,
) -> list[EndpointDoc]:
    child_words = _snake_words(node.name)
    class_path = parent_path
    if not is_root:
        segment = _attr_segment(parent_words, child_words)
        if segment:
            class_path = f"{parent_path}.{segment}"

    methods: list[MethodDoc] = []
    nested: list[EndpointDoc] = []

    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            if item.name == "__init__" or item.name.startswith("_"):
                continue
            params = [
                (arg.arg, _annotation_text(arg))
                for arg in item.args.args
                if arg.arg != "self"
            ]
            http_method, api_path = _collect_http_call(item)
            response_type = _collect_response_type(item)
            methods.append(
                MethodDoc(
                    name=item.name,
                    params=params,
                    http_method=http_method,
                    api_path=api_path,
                    response_type=response_type,
                )
            )
        elif isinstance(item, ast.ClassDef) and item.name.endswith("Endpoint"):
            nested.extend(_parse_endpoint_class(item, child_words, class_path))

    docs = [EndpointDoc(class_name=node.name, client_path=class_path, methods=methods)]
    docs.extend(nested)
    return docs


def _parse_endpoint_module(path: Path) -> tuple[list[EndpointDoc], dict[str, list[ModelField]]]:
    module_ast = ast.parse(path.read_text(encoding="utf-8"))
    model_schemas = _collect_model_schemas(module_ast)
    root_words = path.stem.split("_")
    base_path = f"client.{path.stem}"
    docs: list[EndpointDoc] = []

    for item in module_ast.body:
        if isinstance(item, ast.ClassDef) and item.name.endswith("Endpoint"):
            docs.extend(_parse_endpoint_class(item, root_words, base_path, is_root=True))

    return docs, model_schemas


def _render_endpoint_method(
    endpoint: EndpointDoc,
    method: MethodDoc,
    models: dict[str, list[ModelField]],
) -> list[str]:
    lines = [f"### `{endpoint.client_path}.{method.name}`", ""]

    if method.http_method and method.api_path:
        lines.append(f"- API call: `{method.http_method} {method.api_path}`")
        lines.append("")

    if method.params:
        lines.append("Parameters:")
        lines.append("")
        for name, ann in method.params:
            ann_text = ann or "Any"
            lines.append(f"- `{name}`: `{ann_text}`")
        lines.append("")

    if method.response_type:
        lines.append(f"Response type: `ApiResponse[{method.response_type}]`")
        lines.append("")

    lines.append("Expected response format:")
    lines.append("")
    lines.append("```json")
    lines.append(_render_response_json(method, models))
    lines.append("```")
    lines.append("")

    lines.extend(
        [
            "Example:",
            "",
            "```python",
            "from ponika import PonikaClient",
            "",
            "client = PonikaClient(",
            '    host="192.168.1.1",',
            '    username="admin",',
            '    password="password",',
            "    verify_tls=False,",
            ")",
            "",
            f"response = {endpoint.client_path}.{_method_call(method)}",
            "",
            "if response.success and response.data:",
            "    print(response.data)",
            "else:",
            "    print(response.errors)",
            "```",
            "",
        ]
    )

    return lines


def _render_endpoint_page(
    module_ident: str,
    endpoints: list[EndpointDoc],
    models: dict[str, list[ModelField]],
) -> str:
    lines = [
        f"# `{module_ident}`",
        "",
        "This page is generated from endpoint classes and methods in the codebase.",
        "",
        # f"::: {module_ident}",
        "",
        "## Endpoint Methods",
        "",
    ]

    for endpoint in endpoints:
        if not endpoint.methods:
            continue
        for method in endpoint.methods:
            lines.extend(_render_endpoint_method(endpoint, method, models))

    return "\n".join(lines)


def _iter_core_modules(src_root: Path) -> list[str]:
    modules: list[str] = []
    for path in sorted(src_root.glob("*.py")):
        if path.name.startswith("test_"):
            continue
        if path.name.startswith("__") and path.name != "__init__.py":
            continue
        if path.name == "__init__.py":
            modules.append("ponika")
        else:
            modules.append(f"ponika.{path.stem}")
    return modules


def _render_reference_index(core_modules: list[str], endpoint_modules: list[str]) -> str:
    lines = [
        "# API Reference",
        "",
        "This section is generated from `src/ponika`.",
        "",
        "## Core Modules",
        "",
    ]

    for ident in core_modules:
        lines.append(f"### `{ident}`")
        lines.append("")
        lines.append(f"::: {ident}")
        lines.append("")

    lines.extend(
        [
            "## Endpoint Modules",
            "",
            "Detailed endpoint pages (methods + examples):",
            "",
        ]
    )

    for ident in endpoint_modules:
        slug = ident.rsplit(".", 1)[-1]
        lines.append(f"- [{ident}](endpoints/{slug}.md)")

    lines.append("")
    return "\n".join(lines)


def _render_endpoints_index(endpoint_modules: list[str]) -> str:
    lines = [
        "# Endpoint Reference",
        "",
        "Endpoint modules map to specific areas of the Teltonika API and contain endpoint classes with methods for interacting with those APIs. Each method corresponds to one or more API calls, and the documentation includes details on parameters, response formats, and example usage.",
        "",
    ]
    for ident in endpoint_modules:
        slug = ident.rsplit(".", 1)[-1]
        lines.append(f"- [{ident}]({slug}.md)")
    lines.append("")
    return "\n".join(lines)


def on_config(config):
    root = Path(config.config_file_path).resolve().parent
    src_root = root / "src" / "ponika"
    endpoint_root = src_root / "endpoints"
    reference_root = root / "docs" / "reference"
    endpoints_docs_root = reference_root / "endpoints"

    endpoints_docs_root.mkdir(parents=True, exist_ok=True)
    for stale in endpoints_docs_root.glob("*.md"):
        stale.unlink()

    endpoint_modules: list[str] = []
    for path in sorted(endpoint_root.glob("*.py")):
        if path.name == "__init__.py":
            continue
        module_ident = f"ponika.endpoints.{path.stem}"
        endpoint_modules.append(module_ident)
        endpoint_docs, model_schemas = _parse_endpoint_module(path)
        doc_path = endpoints_docs_root / f"{path.stem}.md"
        doc_path.write_text(
            _render_endpoint_page(module_ident, endpoint_docs, model_schemas),
            encoding="utf-8",
        )

    (endpoints_docs_root / "index.md").write_text(
        _render_endpoints_index(endpoint_modules), encoding="utf-8"
    )

    core_modules = _iter_core_modules(src_root)
    (reference_root / "index.md").write_text(
        _render_reference_index(core_modules, endpoint_modules), encoding="utf-8"
    )

    return config
