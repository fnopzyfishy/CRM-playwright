import allure

from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger(__name__)


class FileInput(BaseElement):
    @property
    def type_of(self):
        return 'file'

    def set_input_files(self, file: str, nth: int = 0, **kwargs) -> None:
        step = f'Set file "{file}" to the {self.type_of} "{self.name}"'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            locator.set_input_files(file)