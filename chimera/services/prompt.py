import aiofiles

from chimera.settings import BASE_DIR


async def get_prompt(name: str, **kwargs) -> str:
    async with aiofiles.open(BASE_DIR / "chimera" / "services" / "prompts" / f"{name}.md") as file:
        content = await file.read()
    if kwargs:
        return content.format(**kwargs)
    return content
