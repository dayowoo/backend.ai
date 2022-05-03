import ast
import logging
import pkg_resources
from pathlib import Path
from typing import Container, Iterator


log = logging.getLogger(__name__)


def scan_entrypoints(
    group_name: str,
    blocklist: Container[str] = None,
) -> Iterator[pkg_resources.EntryPoint]:
    if blocklist is None:
        blocklist = set()
    for entrypoint in scan_entrypoint_from_buildscript(group_name):
        if entrypoint.name in blocklist:
            continue
        yield entrypoint
    for entrypoint in scan_entrypoint_from_package_metadata(group_name):
        if entrypoint.name in blocklist:
            continue
        yield entrypoint


def scan_entrypoint_from_package_metadata(group_name: str) -> Iterator[pkg_resources.EntryPoint]:
    for entrypoint in pkg_resources.iter_entry_points(group_name):
        yield entrypoint


def scan_entrypoint_from_buildscript(group_name: str) -> Iterator[pkg_resources.EntryPoint]:
    ai_backend_ns_path = Path(__file__).parent.parent
    print("Namespace path:", ai_backend_ns_path)
    print("All BUILD files:\n", [*ai_backend_ns_path.glob("**/BUILD")])
    for buildscript_path in ai_backend_ns_path.glob("**/BUILD"):
        log.debug("reading entry points [{}] from {}", group_name, buildscript_path)
        yield from extract_entrypoints_from_buildscript(group_name, buildscript_path)


def extract_entrypoints_from_buildscript(
    group_name: str,
    buildscript_path: Path,
) -> Iterator[pkg_resources.EntryPoint]:
    tree = ast.parse(buildscript_path.read_bytes())
    for node in tree.body:
        if (
            isinstance(node, ast.Expr) and
            isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Name) and
            node.value.func.id == "python_distribution"
        ):
            for kwarg in node.value.keywords:
                if kwarg.arg == "entry_points":
                    raw_data = ast.literal_eval(kwarg.value)
                    for key, raw_entry_points in raw_data.items():
                        if key != group_name:
                            continue
                        for name, ref in raw_entry_points.items():
                            try:
                                yield pkg_resources.EntryPoint.parse(f"{name}={ref}")
                            except ValueError:
                                pass