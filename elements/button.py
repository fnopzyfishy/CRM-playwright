import allure
from playwright.sync_api import expect

from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger(__name__)


class Button(BaseElement):
    @property
    def type_of(self):
        return 'button'

    def check_enabled(self, nth: int = 0, **kwargs) -> None:
        step = f'Checking that {self.type_of} "{self.name}" is enabled'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            expect(locator).to_be_enabled()

    def check_disabled(self, nth: int = 0, **kwargs) -> None:
        step = f'Checking that {self.type_of} "{self.name}" is disabled'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            expect(locator).to_be_disabled()