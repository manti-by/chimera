import asyncio
import sys
from pathlib import Path


async def live_stream(
    stream: asyncio.StreamReader, result: list[str] | None = None, disable_stdio: bool = False
) -> None:
    while True:
        if not (line := await stream.readline()):
            break

        decoded = line.decode()
        if result is not None:
            result.append(decoded)

        if not disable_stdio:
            sys.stdout.write(decoded)
            sys.stdout.flush()


async def is_package_installed(target_path: Path, package_name: str) -> bool:
    from chimera.services.subprocess import run_command
    from chimera.settings import UV

    _, result, _ = await run_command(
        command=[str(UV["path"]), "tree", "--quiet", "--package", package_name],
        target_path=target_path,
        disable_stdio=True,
    )
    return result != ""


async def merge_review_results(results: list[tuple[int, str, str]]) -> tuple[int, str, str]:
    exit_code, stdout, stderr = 0, "", ""
    for c, o, e in results:
        exit_code += c
        stdout += f"\n{o.strip()}" if o.strip() else ""
        stderr += f"\n{e.strip()}" if e.strip() else ""
    return exit_code, stdout, stderr
