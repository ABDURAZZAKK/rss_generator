import re
from bs4 import BeautifulSoup
import rfeed
import aiohttp


class Parser2Ch():
    __url = "https://2ch.hk/"

    async def _get_board_html(self, boardname) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__url + boardname + "/") as resp:
                html = await resp.text()
                return html

    async def parse_and_save_rss(self, boardname) -> str:
        boardname = "".join(re.split("[^a-zA-Z]*", boardname))


        HTML = await self._get_board_html(boardname)
        soup = BeautifulSoup(HTML, "html.parser")
        _items = []
        for div in soup.find_all("div", {"class": "thread"})[1:]:
            thred_link = div.find("a", {"class":"post__reflink"})["href"]
            thred_image_link = div.find("a", {"class":"post__image-link"})["href"]
            thred_title = div.find("article", {"class":"post__message post__message_op"}).text.strip()

            item = rfeed.Item(
                title=thred_title,
                link=thred_link,
                author = "Аноним",
                guid = rfeed.Guid(thred_link),
                enclosure=rfeed.Enclosure(url=thred_image_link,type="image/jpeg",length=0)
            )

            _items.append(item)
        feed = rfeed.Feed(title="Двач",
            description = "",
            language="ru-RU",
            items=_items,
            link=f"https://2ch.hk/{boardname}/" 
        )
        rss = feed.rss()

        return rss
    








