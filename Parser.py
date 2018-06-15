import asyncio
import ParseCity

from pyppeteer.errors import ElementHandleError
from pyppeteer import launch

eventid = []


async def main():
    browser = await launch()
    page = await browser.newPage()
    with open("maindata.txt", "w", errors="ignore", encoding="UTF-8") as file:
        for event_number in eventid:
            print(event_number)
            await page.goto('https://2event.com/uk/events/' + event_number)
            await page.waitForSelector(".event-address-street")

            # місце
            element = await page.querySelector('p.event-address-street')
            title = await page.evaluate('(element) => element.textContent',
                                        element)
            file.write(title.strip() + "@@")

            # назва
            element = await page.querySelector('h1.location-title')
            title = await page.evaluate('(element) => element.textContent',
                                        element)
            file.write(title.strip() + "@@")

            # категорія
            element = await page.querySelector('p.location-category')
            title = await page.evaluate('(element) => element.textContent',
                                        element)
            file.write(title.strip() + "@@")

            # ссилка в фейсбук
            try:
                element = await page.querySelector('a.fb')
                title = await page.evaluate(
                    '(element) => element.getAttribute(\'href\')', element)
                file.write(title.strip() + "@@")
            except ElementHandleError:
                title = ""
                file.write(title + "@@")

            # дата
            element = await page.querySelector('div.event-date')
            title = await page.evaluate('(element) => element.textContent',
                                        element)
            title = title.strip().split("                                ")
            file.write(title[0].strip() + "@@" + title[1] + "@@")

            # опис
            element = await page.querySelector('div.text-description-content')
            title = await page.evaluate('(element) => element.textContent',
                                        element)
            file.write(title.strip() + "####")

    await browser.close()

def start():
    global eventid
    eventid=ParseCity.main()
    asyncio.get_event_loop().run_until_complete(main())