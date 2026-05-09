from playwright.sync_api import Page
import allure
from pages.base_page import BasePage
from common.config_reader import ConfigReader
from common.logger import get_logger

logger = get_logger()


class LoginPage(BasePage):
    """登录页面封装 — 适配 zltquant.com"""

    # === 首页登录入口 ===
    LOGIN_ENTRY_BUTTON = "button:has-text('登录')"

    # === 弹窗/登录表单内元素 ===
    PASSWORD_LOGIN_TAB = "text=密码登录"
    USERNAME_INPUT = "input[placeholder='请输入用户名']"
    PASSWORD_INPUT = "input[placeholder='请输入登录密码']"
    DIALOG_LOGIN_BUTTON = ".el-dialog button:has-text('登录'), .login-dialog button:has-text('登录'), form button:has-text('登录')"
    ERROR_MESSAGE = ".el-message__content, .error-msg, .ant-message-error"

    # === 登录成功后页面标识 ===
    USER_AVATAR = ".avatar, .user-avatar, .user-info"

    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = ConfigReader.get_base_url()

    @allure.step("打开首页并点击登录入口")
    def open(self):
        """打开首页，等待登录入口加载"""
        self.navigate(self.base_url)
        self.page.wait_for_load_state("networkidle")
        logger.info(f"Opened homepage: {self.base_url}")
        return self

    @allure.step("点击顶部登录按钮，唤起登录弹窗")
    def click_login_entry(self):
        """点击首页的登录入口按钮"""
        # 首页可能有多个含"登录"文字的按钮，优先取可见的
        self.page.locator(self.LOGIN_ENTRY_BUTTON).first.click()
        logger.info("Clicked login entry button")
        return self

    @allure.step("切换到密码登录 Tab")
    def switch_to_password_login(self):
        """点击'密码登录'切换到账号密码登录方式"""
        if self.is_visible(self.PASSWORD_LOGIN_TAB):
            self.click(self.PASSWORD_LOGIN_TAB)
            logger.info("Switched to password login tab")
        return self

    @allure.step("输入用户名: {username}")
    def input_username(self, username: str):
        """输入用户名"""
        self.fill(self.USERNAME_INPUT, username)
        return self

    @allure.step("输入密码")
    def input_password(self, password: str):
        """输入密码"""
        self.fill(self.PASSWORD_INPUT, password)
        return self

    @allure.step("点击弹窗内的登录按钮")
    def click_dialog_login(self):
        """点击登录弹窗/表单中的登录按钮"""
        self.page.locator(self.DIALOG_LOGIN_BUTTON).first.click()
        self.page.wait_for_load_state("networkidle")
        logger.info("Clicked dialog login button")
        return self

    @allure.step("执行完整登录流程: {username}")
    def login(self, username: str = None, password: str = None):
        """完整登录流程：打开首页 → 点击登录 → 切Tab → 填账号密码 → 点击登录"""
        if username is None:
            username = ConfigReader.get_username()
        if password is None:
            password = ConfigReader.get_password()

        self.open()
        self.click_login_entry()
        self.switch_to_password_login()
        self.input_username(username)
        self.input_password(password)
        self.click_dialog_login()
        logger.info(f"Login attempt with username: {username}")
        return self

    def is_login_success(self) -> bool:
        """判断是否登录成功（检查用户头像等标识）"""
        try:
            self.page.wait_for_selector(self.USER_AVATAR, timeout=3000)
            logger.info("Login success detected")
            return True
        except:
            logger.warning("Login success indicator not found")
            return False

    def get_error_message(self) -> str:
        """获取错误提示信息"""
        if self.is_visible(self.ERROR_MESSAGE):
            msg = self.get_text(self.ERROR_MESSAGE)
            logger.info(f"Error message: {msg}")
            return msg
        return ""

    def is_at_login_page(self) -> bool:
        """判断登录弹窗是否仍可见"""
        return self.is_visible(self.DIALOG_LOGIN_BUTTON)
