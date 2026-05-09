import os
import pytest
from playwright.sync_api import Page, expect
import allure
from common.logger import get_logger
from common.config_reader import ConfigReader

logger = get_logger()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文参数，开启视频录制"""
    video_dir = os.path.join(os.path.dirname(__file__), "reports", "videos")
    os.makedirs(video_dir, exist_ok=True)

    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
        "record_video_dir": video_dir,
        "record_video_size": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="function")
def page(page: Page):
    """每个测试用例的页面fixture，自动设置默认超时"""
    timeout = ConfigReader.get_timeout()
    page.set_default_timeout(timeout)
    logger.info(f"Page initialized with timeout {timeout}ms")
    yield page


@pytest.fixture(scope="function")
def goto_base_url(page: Page):
    """导航到基础URL"""
    base_url = ConfigReader.get_base_url()
    logger.info(f"Navigating to {base_url}")
    page.goto(base_url)
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图并附加到allure报告"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                screenshot_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
                page.screenshot(path=screenshot_path, full_page=True)
                allure.attach.file(screenshot_path, name="失败截图", attachment_type=allure.attachment_type.PNG)
                logger.error(f"Test failed, screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")


@pytest.fixture
def faker_utils():
    """提供Faker工具类"""
    from common.faker_utils import FakerUtils
    return FakerUtils()
