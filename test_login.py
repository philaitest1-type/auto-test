import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://playwright-demo.eventos.work/web/portal/529/event/3988"
LOGIN_URL = f"{BASE_URL}/users/login"

VALID_EMAIL = "philaitest1@gmail.com"
VALID_PASSWORD = "12345678!"
WRONG_PASSWORD = "wrongpassword1!"
UNREGISTERED_EMAIL = "notregistered@example.com"


@pytest.fixture(autouse=True)
def go_to_login(page: Page):
    page.goto(LOGIN_URL)
    page.wait_for_load_state("networkidle")


# ── 画面遷移--21 ──────────────────────────────────────────────
def test_navigate_to_login_from_top_via_ticket_button(page: Page):
    """TOP画面から「チケット申し込み」ボタンを押すとログイン画面へ遷移すること"""
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    # TOPページが直接ログインへリダイレクトする場合もある
    ticket_btn = page.locator("button, a").filter(has_text="チケット申し込み")
    if ticket_btn.count() > 0:
        ticket_btn.first.click()
        page.wait_for_load_state("networkidle")
    assert "/login" in page.url, f"Expected /login in URL but got: {page.url}"


# ── 画面遷移--19 ──────────────────────────────────────────────
def test_url_contains_login(page: Page):
    """PC版でURLに「/login」が含まれること"""
    assert "/login" in page.url


# ── 画面遷移--18 ──────────────────────────────────────────────
def test_page_title_element_displayed(page: Page):
    """ログイン画面タイトル要素が表示されること"""
    # タイトル要素が存在すること（テキストはイベント設定に依存）
    expect(page.locator(".title__content__text")).to_be_visible()


# ── 画面遷移--17 ──────────────────────────────────────────────
def test_email_field_displayed(page: Page):
    """メールアドレスラベルとテキストボックスが表示されること"""
    expect(page.locator(".login-form__mail__label")).to_contain_text("メールアドレス")
    expect(page.locator("#mail_address")).to_be_visible()


# ── 画面遷移--16 ──────────────────────────────────────────────
def test_email_field_accepts_input(page: Page):
    """メールアドレス欄に文字入力でき、入力した文字が表示されること"""
    page.locator("#mail_address").fill("test@test.com")
    expect(page.locator("#mail_address")).to_have_value("test@test.com")


# ── 画面遷移--15 ──────────────────────────────────────────────
def test_email_valid_lowercase(page: Page):
    """abc@gmail.com を入力すると入力した文字が表示されること"""
    page.locator("#mail_address").fill("abc@gmail.com")
    expect(page.locator("#mail_address")).to_have_value("abc@gmail.com")


# ── 画面遷移--14 ──────────────────────────────────────────────
def test_email_valid_uppercase(page: Page):
    """ABC@GMAIL.COM を入力すると入力した文字が表示されること"""
    page.locator("#mail_address").fill("ABC@GMAIL.COM")
    expect(page.locator("#mail_address")).to_have_value("ABC@GMAIL.COM")


# ── 画面遷移--13 ──────────────────────────────────────────────
def test_email_invalid_missing_tld(page: Page):
    """abc@gmail でエラー「メールアドレスが正しくありません」が表示されること"""
    page.locator("#mail_address").fill("abc@gmail")
    page.locator("#mail_address").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text("メールアドレスが正しくありません")


# ── 画面遷移--12 ──────────────────────────────────────────────
def test_email_invalid_special_char_before_at(page: Page):
    """abc!@gmail.com でエラー「メールアドレスが正しくありません」が表示されること"""
    page.locator("#mail_address").fill("abc!@gmail.com")
    page.locator("#mail_address").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text("メールアドレスが正しくありません")


# ── 画面遷移--11 ──────────────────────────────────────────────
def test_email_invalid_no_at_sign(page: Page):
    """test.abc でエラー「メールアドレスが正しくありません」が表示されること"""
    page.locator("#mail_address").fill("test.abc")
    page.locator("#mail_address").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text("メールアドレスが正しくありません")


# ── 画面遷移--10 ──────────────────────────────────────────────
def test_email_invalid_starts_with_at(page: Page):
    """@gmail.com でエラー「メールアドレスが正しくありません」が表示されること"""
    page.locator("#mail_address").fill("@gmail.com")
    page.locator("#mail_address").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text("メールアドレスが正しくありません")


# ── 画面遷移--9 ──────────────────────────────────────────────
def test_email_invalid_fullwidth_chars(page: Page):
    """全角文字入力でエラー「メールアドレスが正しくありません」が表示されること"""
    page.locator("#mail_address").fill("テスト@gmail.com")
    page.locator("#mail_address").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text("メールアドレスが正しくありません")


# ── 画面遷移--8 ──────────────────────────────────────────────
def test_email_empty_shows_required_error(page: Page):
    """メールアドレスをクリアするとエラー「メールアドレスを入力してください」が表示されること"""
    page.locator("#mail_address").fill("abc@gmail.com")
    page.locator("#mail_address").fill("")
    page.locator("#mail_address").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text("メールアドレスを入力してください")


# ── 画面遷移--7 ──────────────────────────────────────────────
def test_password_field_displayed(page: Page):
    """パスワードラベル、テキストボックス、マスクアイコンが表示されること"""
    expect(page.locator(".login-form__password__label")).to_contain_text("パスワード")
    expect(page.locator("#password")).to_be_visible()
    expect(page.locator("button[aria-label='append icon']")).to_be_visible()


# ── 画面遷移--6 ──────────────────────────────────────────────
def test_password_is_masked_by_default(page: Page):
    """パスワード入力時、マスク表示（type=password）されること"""
    page.locator("#password").fill("TestPass1!")
    expect(page.locator("#password")).to_have_attribute("type", "password")


# ── 画面遷移--5 ──────────────────────────────────────────────
def test_password_unmask_on_eye_icon_click(page: Page):
    """目アイコンを押すとマスク表示が解除されること"""
    page.locator("#password").fill("TestPass1!")
    page.locator("button[aria-label='append icon']").click()
    page.wait_for_timeout(300)
    expect(page.locator("#password")).to_have_attribute("type", "text")


# ── 画面遷移--4 ──────────────────────────────────────────────
def test_password_remask_on_second_eye_icon_click(page: Page):
    """目アイコンを2回押すと再びマスク表示されること"""
    page.locator("#password").fill("TestPass1!")
    eye_btn = page.locator("button[aria-label='append icon']")
    eye_btn.click()
    page.wait_for_timeout(300)
    eye_btn.click()
    page.wait_for_timeout(300)
    expect(page.locator("#password")).to_have_attribute("type", "password")


# ── 画面遷移--3 ──────────────────────────────────────────────
def test_password_too_short_shows_error(page: Page):
    """8文字以下のパスワードでエラー「パスワードは8文字以上32文字以下で指定してください」が表示されること"""
    page.locator("#password").fill("Ab1!")
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text(
        "パスワードは8文字以上32文字以下で指定してください"
    )


# ── 画面遷移--2 ──────────────────────────────────────────────
def test_password_max_32_chars(page: Page):
    """32文字以上入力するとエラーメッセージが表示されること"""
    page.locator("#password").fill("A" * 33)
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message").first).to_contain_text(
        "パスワードは8文字以上32文字以下で指定してください"
    )


# ── 画面遷移--1 ──────────────────────────────────────────────
def test_password_numbers_only_no_error(page: Page):
    """数字のみパスワードでエラーメッセージが表示されないこと"""
    page.locator("#password").fill("12345678")
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message")).not_to_be_visible()


# ── 画面遷移-0 ──────────────────────────────────────────────
def test_password_letters_only_no_error(page: Page):
    """英大文字・英小文字のみパスワードでエラーメッセージが表示されないこと"""
    page.locator("#password").fill("AbCdEfGh")
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message")).not_to_be_visible()


# ── 画面遷移-1 ──────────────────────────────────────────────
def test_password_symbols_only_no_error(page: Page):
    """記号のみパスワードでエラーメッセージが表示されないこと"""
    page.locator("#password").fill("!@#$%^&*")
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message")).not_to_be_visible()


# ── 画面遷移-2 ──────────────────────────────────────────────
def test_password_numbers_and_letters_no_error(page: Page):
    """数字と英大文字・英小文字の組み合わせでエラーが表示されないこと"""
    page.locator("#password").fill("Abc12345")
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message")).not_to_be_visible()


# ── 画面遷移-3 ──────────────────────────────────────────────
def test_password_numbers_and_symbols_no_error(page: Page):
    """数字と記号の組み合わせでエラーが表示されないこと"""
    page.locator("#password").fill("1234!@#$")
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message")).not_to_be_visible()


# ── 画面遷移-4 ──────────────────────────────────────────────
def test_password_symbols_and_letters_no_error(page: Page):
    """記号と英大文字・英小文字の組み合わせでエラーが表示されないこと"""
    page.locator("#password").fill("Abcd!@#$")
    page.locator("#password").blur()
    page.wait_for_timeout(500)
    expect(page.locator(".v-messages__message")).not_to_be_visible()


# ── 画面遷移-5 ──────────────────────────────────────────────
def test_forgot_password_link_displayed(page: Page):
    """「パスワードを忘れた場合」テキストが表示されること"""
    expect(page.locator(".smart__forget__link")).to_contain_text("パスワードを忘れた場合")


# ── 画面遷移-6 ──────────────────────────────────────────────
def test_forgot_password_link_navigates(page: Page):
    """「パスワードを忘れた場合」を押下するとパスワード再設定画面に遷移すること"""
    page.locator(".smart__forget__link").click()
    page.wait_for_url(lambda url: "reset" in url or "password" in url or "forgot" in url or "remind" in url, timeout=10000)
    assert (
        "password" in page.url
        or "reset" in page.url
        or "forgot" in page.url
        or "remind" in page.url
    ), f"Expected password reset URL but got: {page.url}"


# ── 画面遷移-7 ──────────────────────────────────────────────
def test_login_button_displayed(page: Page):
    """ログインボタンが表示されること"""
    expect(page.locator("#login_button")).to_be_visible()
    expect(page.locator("#login_button")).to_contain_text("ログイン")


# ── 画面遷移-8 ──────────────────────────────────────────────
def test_login_fails_wrong_password(page: Page):
    """正しいメールアドレス・間違ったパスワードでログイン失敗しエラーメッセージが表示されること"""
    page.locator("#mail_address").fill(VALID_EMAIL)
    page.locator("#password").fill(WRONG_PASSWORD)
    page.locator("#login_button").click()
    page.wait_for_timeout(3000)
    expect(page.locator("text=ログインできませんでした")).to_be_visible()


# ── 画面遷移-9 ──────────────────────────────────────────────
def test_login_fails_unregistered_email(page: Page):
    """未登録メールアドレス・正しいパスワードでログイン失敗しエラーメッセージが表示されること"""
    page.locator("#mail_address").fill(UNREGISTERED_EMAIL)
    page.locator("#password").fill(VALID_PASSWORD)
    page.locator("#login_button").click()
    page.wait_for_timeout(3000)
    expect(page.locator("text=ログインできませんでした")).to_be_visible()


# ── 画面遷移-10 ──────────────────────────────────────────────
def test_login_success_valid_credentials(page: Page):
    """正しいメールアドレスとパスワードでログインしプロファイル画面へ遷移すること"""
    page.locator("#mail_address").fill(VALID_EMAIL)
    page.locator("#password").fill(VALID_PASSWORD)
    page.locator("#login_button").click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=10000)
    assert "/login" not in page.url, f"Login failed, still on login page: {page.url}"


# ── 画面遷移-11 ──────────────────────────────────────────────
def test_register_button_displayed(page: Page):
    """「新規登録」ボタンが表示されること"""
    expect(page.locator("#register_button")).to_be_visible()
    expect(page.locator("#register_button")).to_contain_text("新規登録")


# ── 画面遷移-12 ──────────────────────────────────────────────
def test_register_button_navigates(page: Page):
    """「新規登録」ボタンを押下すると新規登録画面に遷移すること"""
    page.locator("#register_button").click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=10000)
    assert "/login" not in page.url, f"Expected to navigate away from login but got: {page.url}"


# ── 画面遷移-13 ──────────────────────────────────────────────
def test_scroll_up_to_top(page: Page):
    """最下部から上へスクロールして最上部まで到達できること"""
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.evaluate("window.scrollTo(0, 0)")
    assert page.evaluate("window.scrollY") == 0


# ── 画面遷移-14 ──────────────────────────────────────────────
def test_scroll_down_to_bottom(page: Page):
    """最上部から下へスクロールして最下部まで到達できること"""
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    scroll_y = page.evaluate("window.scrollY")
    scroll_max = page.evaluate("document.body.scrollHeight - window.innerHeight")
    assert scroll_y >= scroll_max - 5


# ── 画面遷移-15 ──────────────────────────────────────────────
def test_scroll_up_and_down(page: Page):
    """上下スクロールができること"""
    page.evaluate("window.scrollTo(0, 200)")
    assert page.evaluate("window.scrollY") >= 0
    page.evaluate("window.scrollTo(0, 0)")
    assert page.evaluate("window.scrollY") == 0
