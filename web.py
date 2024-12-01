from parser_2ch import Parser2Ch
from litestar import Litestar, get


@get("/2ch/{boardname:str}/rss")
async def rss2ch(boardname: str) -> dict[str, str]:
    p = Parser2Ch()
    rss = await p.parse_and_save_rss(boardname)
    return rss


app = Litestar(
    route_handlers=[rss2ch]
               )
