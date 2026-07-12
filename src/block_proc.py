



def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str]= []

    raw_blocks: list[str] = markdown.split('\n\n')

    for raw_block in raw_blocks:
        raw_block = raw_block.strip()
        if not raw_block:
            continue
        blocks.append(raw_block)
    
    return blocks