import aiofiles

from chimera.settings import BASE_PATH


async def get_prompt(name: str, **kwargs) -> str:
    async with aiofiles.open(BASE_PATH / "chimera" / "services" / "prompts" / f"{name}.md") as file:
        content = await file.read()
    if kwargs:
        return content.format(**kwargs)
    return content
