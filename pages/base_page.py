from playwright.sync_api import Page, Locator, expect
import allure
from common.logger import get_logger

logger = get_logger()


class BasePage:
    """页面基类，封装常用操作"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = logger

    def navigate(self, url: str):
        """导航到指定URL"""
        self.logger.info(f"Navigating to: {url}")
        with allure.step(f"访问页面: {url}"):
            self.page.goto(url)

    def find(self, selector: str) -> Locator:
        """查找元素"""
        return self.page.locator(selector)

    def click(self, selector: str, force: bool = False):
        """点击元素"""
        self.logger.info(f"Clicking element: {selector}")
        with allure.step(f"点击元素: {selector}"):
            self.page.locator(selector).click(force=force)

    def fill(self, selector: str, value: str):
        """填充输入框"""
        self.logger.info(f"Filling {selector} with value: {value}")
        with allure.step(f"输入内容到 {selector}"):
            self.page.locator(selector).fill(value)

    def type(self, selector: str, value: str, delay: int = 50):
        """模拟键盘输入"""
        self.logger.info(f"Typing into {selector}")
        with allure.step(f"键入内容到 {selector}"):
            self.page.locator(selector).type(value, delay=delay)

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        text = self.page.locator(selector).inner_text()
        self.logger.info(f"Element {selector} text: {text}")
        return text

    def is_visible(self, selector: str) -> bool:
        """判断元素是否可见"""
        return self.page.locator(selector).is_visible()

    def wait_for_selector(self, selector: str, timeout: int = None):
        """等待元素出现"""
        self.logger.info(f"Waiting for element: {selector}")
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    def expect_visible(self, selector: str):
        """断言元素可见"""
        with allure.step(f"断言元素可见: {selector}"):
            expect(self.page.locator(selector)).to_be_visible()

    def expect_contains_text(self, selector: str, text: str):
        """断言元素包含指定文本"""
        with allure.step(f"断言 {selector} 包含文本: {text}"):
            expect(self.page.locator(selector)).to_contain_text(text)

    def screenshot(self, name: str = "screenshot"):
        """截图并附加到allure报告"""
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)

    def get_current_url(self) -> str:
        """获取当前页面URL"""
        return self.page.url

    def scroll_to(self, selector: str):
        """滚动到指定元素"""
        self.page.locator(selector).scroll_into_view_if_needed()

    def hover(self, selector: str):
        """鼠标悬停"""
        self.page.locator(selector).hover()

    def select_option(self, selector: str, value: str):
        """选择下拉框选项"""
        self.page.locator(selector).select_option(value)
