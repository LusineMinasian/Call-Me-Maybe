import json
from typing import Any, TypeVar
from pydantic import BaseModel, ValidationError
from .models import FunctionDefinition, PromptItem

ModelT = TypeVar("ModelT", bound=BaseModel)


def read_json(path: str) -> Any:
    try:
        with open(path, encoding="utf-8-sig") as file:
            return json.load(file)
    except OSError as error:
        raise ValueError(f"cannot read {path}: {error.strerror}") from error
    except UnicodeDecodeError as error:
        raise ValueError(f"{path} is not a UTF-8 text file") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{path} is not valid JSON "
            f"(line {error.lineno}, column {error.colno}: {error.msg})"
        ) from error


def _describe(error: ValidationError) -> str:
    problems = []
    for problem in error.errors():
        where = ".".join(str(part) for part in problem["loc"])
        problems.append(f"{where or 'value'}: {problem['msg']}")
    return "; ".join(problems)


def _parse_items(data: Any, model: type[ModelT], path: str) -> list[ModelT]:
    if not isinstance(data, list):
        raise ValueError(f"{path}: the top level must be a JSON array")
    items: list[ModelT] = []
    for index, raw in enumerate(data):
        try:
            items.append(model.model_validate(raw))
        except ValidationError as error:
            raise ValueError(
                f"{path}: element {index}: {_describe(error)}"
            ) from error
    return items


def load_functions(path: str) -> list[FunctionDefinition]:
    functions = _parse_items(_read_json(path), FunctionDefinition, path)
    if not functions:
        raise ValueError(f"{path}: no function is defined")
    names = [function.name for function in functions]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(
            f"{path}: duplicate function names: {', '.join(duplicates)}"
        )
    return functions


def load_prompts(path: str) -> list[PromptItem]:
    return _parse_items(_read_json(path), PromptItem, path)
