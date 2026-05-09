import os
import pytest
import allure
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from common.logger import get_logger

logger = get_logger()


@allure.feature("登录功能")
@allure.story("登录成功场景")
class TestLoginSuccess:
    """登录成功测试用例"""

    @allure.title("使用正确的账号密码登录成功")
    @allure.description("验证输入正确的用户名和密码后，可以正常登录并跳转到首页")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_valid_credentials(self, page: Page):
        """测试用例：正确的用户名和密码登录成功"""
        # 从环境变量获取账号（避免硬编码）
        username = os.getenv("TEST_USERNAME", "")
        password = os.getenv("TEST_PASSWORD", "")

        # 如果没有配置账号，跳过测试并提示
        if not username or not password:
            pytest.skip("未配置测试账号，请设置环境变量 TEST_USERNAME 和 TEST_PASSWORD")

        with allure.step("步骤1: 打开登录页面并执行登录"):
            login_page = LoginPage(page)
            login_page.login(username=username, password=password)

        with allure.step("步骤2: 验证登录成功"):
            # 方式1: 检查页面跳转（URL 不再是登录页）
            current_url = page.url
            logger.info(f"当前页面URL: {current_url}")
            allure.attach(current_url, name="登录后URL", attachment_type=allure.attachment_type.TEXT)

            # 断言：URL 已变化，不再停留在登录页
            assert "/login" not in current_url, f"登录后仍停留在登录页: {current_url}"

        with allure.step("步骤3: 验证登录态（页面包含用户相关元素）"):
            # 方式2: 检查页面上出现用户头像/用户名等元素
            # 根据实际页面结构调整，这里使用几种常见判断
            page.wait_for_timeout(2000)  # 等待页面完全加载

            # 尝试查找用户相关元素（多备几种选择器）
            user_indicators = [
                ".avatar",
                ".user-avatar",
                ".user-info",
                "text=退出",
                "text=个人中心",
                "text=我的",
                ".el-dropdown",
            ]

            found = False
            for selector in user_indicators:
                if page.locator(selector).first.is_visible(timeout=3000):
                    logger.info(f"找到用户标识元素: {selector}")
                    found = True
                    break

            # 截图附加到报告
            screenshot = page.screenshot()
            allure.attach(screenshot, name="登录成功截图", attachment_type=allure.attachment_type.PNG)

            assert found, "登录后未找到用户标识元素，可能登录未成功"

