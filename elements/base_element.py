import allure
from playwright.sync_api import Page, Locator, expect

from tools.logger import get_logger

logger = get_logger(__name__)


class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page
        self.name = name
        self.locator = locator

    @property
    def type_of(self) -> str:
        return "base element"

    def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        return self.page.locator(locator).nth(nth)

    def click(self, nth: int = 0, **kwargs) -> None:
        step = f'Clicking {self.type_of} "{self.name}"'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            locator.click()

    def check_visible(self, nth: int = 0, **kwargs) -> None:
        step = f'Checking that {self.type_of} "{self.name}" is visible'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            expect(locator).to_be_visible()

    def check_have_text(self, text: str, nth: int = 0, **kwargs) -> None:
        step = f'Checking that {self.type_of} "{self.name}" has text "{text}"'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            expect(locator).to_have_text(text)