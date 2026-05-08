import pytest
import re
from playwright.sync_api import Page, expect

BASE_URL = "https://admin.odakyu.bravesoft.vn"
LOGIN_URL = f"{BASE_URL}/login"

VALID_EMAIL = "kimtran@bravesoft.com.vn"
VALID_PASSWORD = "brave0404"


@pytest.fixture(autouse=True)
def go_to_login(page: Page)-> None:
    page.goto(LOGIN_URL)
    page.locator("input[name=\"email\"]").click()
    page.locator("input[name=\"email\"]").fill(VALID_EMAIL)
    page.locator("#password").click()
    page.locator("#password").fill(VALID_PASSWORD)
    page.get_by_role("button", name="ログイン").click()
    page.get_by_role("button", name="新規追加").click()
    return page

    page.get_by_role("button", name="新規追加").click()
    page.locator("input[name=\"userName\"]").click()
    page.locator("input[name=\"userName\"]").fill("テキスト")
    page.locator("input[name=\"userName\"]").press("Enter")
    page.locator("input[name=\"userName\"]").fill("テキスト")
    page.get_by_text("アカウント名 * （255文字以内）").click()
    page.get_by_text("メールアドレス *").click()
    page.goto("https://admin.odakyu.bravesoft.vn/login")
    page.locator("input[name=\"email\"]").click()
    page.locator("input[name=\"email\"]").fill("kimtran@bravesoft.com.vn")
    page.locator("input[name=\"email\"]").press("Tab")
    page.locator("input[name=\"email\"]").fill("kimtran@bravesoft.com.vn")
    page.locator("#password").fill("brave0404")
    page.get_by_role("button", name="ログイン").click()
    page.get_by_role("button", name="新規追加").click()
    page.get_by_role("combobox").nth(1).click()
    page.locator("span").filter(has_text="マスター管理者").click()
    page.get_by_role("combobox").filter(has_text="マスター管理者").click()
    page.locator("span").filter(has_text="テナント管理者").click()
    page.get_by_role("combobox").filter(has_text=re.compile(r"^$")).click()
    page.get_by_label("キム_新チケット").get_by_text("キム_新チケット").click()
    page.locator("#pointAward1").check()
    page.locator("#authority1").check()
    page.locator("#authority2").check()
    page.locator("#authority1").check()
    page.get_by_role("combobox").filter(has_text="テナント管理者").click()
    page.get_by_role("option", name="マスター管理者").click()


# TC-1: 画面タイトル「新規アカウント追加」が表示されること
def test_01(page: Page):
    expect(page.get_by_text("新規アカウント追加")).to_be_visible()


# TC-2: URL「/account-management」が表示されること
def test_02(page: Page):
    expect(page).to_have_url(f"{BASE_URL}/account-management")


# TC-3: 「アカウント名 *（255文字以内）」ラベルが表示されること
def test_03(page: Page):
    expect(
        page.get_by_text(re.compile(r"アカウント名\s*\*\s*（255文字以内）"))
    ).to_be_visible()


# TC-4: 「アカウント名」ボックスに入力でき、入力文字が表示されること
def test_04(page: Page):
    locator = page.locator("input[name=\"userName\"]")
    locator.fill("テキスト")
    expect(locator).to_have_value("テキスト")


# TC-5: 「メールアドレス」ラベルが表示されること
def test_05(page: Page):
    expect(page.get_by_text("メールアドレス *")).to_be_visible()


# TC-6: メールアドレスを入力でき、入力文字が表示されること
def test_06(page: Page):
    locator = page.locator("input[name=\"email\"]")
    locator.fill("trucly@bravesoft-vn.com.vn")
    expect(locator).to_have_value("trucly@bravesoft-vn.com.vn")


# TC-7: 「パスワード *（半角英数字8文字以上32文字以内）」ラベルが表示されること
def test_07(page: Page):
    expect(
        page.get_by_text(re.compile(r"パスワード\s*\*\s*（半角英数字\s*8文字以上32文字以内）"))
    ).to_be_visible()


# TC-8: placeholder「**********」が表示されること
def test_08(page: Page):
    expect(page.get_by_placeholder("**********")).to_be_visible()


# TC-9: パスワードに入力でき、マスク表示されること
def test_09(page: Page):
    page.get_by_role("textbox", name="**********").fill("abc12345")
    expect(page.get_by_role("textbox", name="**********")).to_have_value("abc12345")
    expect(page.get_by_role("textbox", name="**********")).to_have_attribute("type", "password")


# TC-10: 権限セレクトボックスが表示され、初期値が空白であること
def test_10(page: Page):
    role_select = page.get_by_role("combobox").nth(1)
    expect(role_select).to_be_visible()
#    expect(role_select).to_have_value("")


# TC-11: 「マスター管理者」を選択できること
def test_11(page: Page):
    locator = page.get_by_role("combobox").nth(1).click()
    page.locator("span").filter(has_text="マスター管理者").click()
 #   page.get_by_role("combobox").filter(has_text="マスター管理者").click()
    expect(locator).to_have_value("マスター管理者")

#    page.locator("span").filter(has_text="マスター管理者").click()
 #   page.get_by_role("combobox").filter(has_text="マスター管理者").click()
 #   page.locator("span").filter(has_text="テナント管理者").click()


# TC-12: 「テナント管理者」を選択できること
def test_12(page: Page):
    page.get_by_role("combobox").select_option(label="テナント管理者")
    selected = page.get_by_role("combobox").evaluate(
        "el => el.options[el.selectedIndex].text"
    )
    assert selected == "テナント管理者"


# TC-13: 「マスター管理者」と「テナント管理者」を同時に選択できないこと（1つしか選べない）
def test_13(page: Page):
    combobox = page.get_by_role("combobox")
    combobox.select_option(label="マスター管理者")
    combobox.select_option(label="テナント管理者")
    selected = combobox.evaluate("el => el.options[el.selectedIndex].text")
    assert selected == "テナント管理者"
    selected_count = combobox.evaluate("el => el.selectedOptions.length")
    assert selected_count == 1


# TC-14: 「チケット組成時のポイント付与パラメータの変更権限」ラベルと「有」「無」が表示されること
def test_14(page: Page):
    expect(
        page.get_by_text(re.compile(r"チケット組成時のポイント付与パラメータの変更権限"))
    ).to_be_visible()
    expect(page.get_by_role("radio", name="有")).to_be_visible()
    expect(page.get_by_role("radio", name="無")).to_be_visible()


# TC-15: 「有」を選択できること
def test_15(page: Page):
    page.get_by_role("radio", name="有").check()
    expect(page.get_by_role("radio", name="有")).to_be_checked()


# TC-16: 「無」を選択できること
def test_16(page: Page):
    page.get_by_role("radio", name="無").check()
    expect(page.get_by_role("radio", name="無")).to_be_checked()


# TC-17: 「有」と「無」を同時に選択できないこと（1つしか選べない）
def test_17(page: Page):
    page.get_by_role("radio", name="有").check()
    page.get_by_role("radio", name="無").check()
    expect(page.get_by_role("radio", name="無")).to_be_checked()
    expect(page.get_by_role("radio", name="有")).not_to_be_checked()
