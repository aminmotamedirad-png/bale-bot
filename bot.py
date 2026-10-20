import os
import time
import requests

BOT_TOKEN = "1225172136:LZJQJc0gq2ZXXtDubismRVcVPRMtGOOkfRY"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# اگر آیدی با @ جواب نداد، شناسه عددی را جایگزین می‌کنیم
TARGET_CHANNEL = "@helmaorganic"


def send_photo_with_caption(chat_id, photo_path, caption):
    url = f"{BASE_URL}/sendPhoto"
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as img:
            files = {"photo": img}
            data = {"chat_id": chat_id, "caption": caption}
            res = requests.post(url, data=data, files=files)
            print("پاسخ سرور بله برای عکس:", res.text)
            return res.json()
    else:
        print(f"❌ خطا: فایل عکس {photo_path} در پوشه پیدا نشد!")
    return None


def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    res = requests.post(url, json={"chat_id": chat_id, "text": text})
    print("پاسخ سرور بله برای پیام تایید:", res.text)


def main():
    print("بات بله روشن شد... لطفاً در پی‌وی بات کلمه «گردو» را بفرست.")
    last_update_id = 0

    while True:
        try:
            response = requests.get(
                f"{BASE_URL}/getUpdates",
                params={"offset": last_update_id + 1, "timeout": 20},
                timeout=30,
            )
            result = response.json()

            if result.get("ok") and "result" in result:
                for item in result["result"]:
                    last_update_id = item["update_id"]

                    message = item.get("message")
                    if not message or "text" not in message:
                        continue

                    text = message.get("text", "").strip()
                    user_chat_id = message["chat"]["id"]
                    print(f"پیام دریافت شد: «{text}» از چت‌آیدی: {user_chat_id}")

                    if "گردو" in text:
                        print("دستور گردو تشخیص داده شد. در حال ارسال...")
                        caption = """#گردو_درجه_یک و اعلا شارژ شد 🥳🥳🥳

*گردو پوست نازک بسیار خوش طعم و چرب با ۸۰

 درصد مغز سفید شارژ شد*🎊🎊😍😍😍🥳🥳🥳

*################*
قیمت بازار  کیلوی ی تومن  
خیلی زیاده
‌
حالا قیمت ما رو ببینید  🤩🤩⬇️⬇️

✅✅*قیمت با تخفیف ویژه هر کیلو890هزار تومان✅✅

#################*

پشتیبان ثبت سفارش ⬇️⬇️⬇️⬇️⬇️

آیدی ثبت سفارش ⬅️  @adminhelmaorganic

شماره موبایل ثبت سفارش⬅️   09170889337"""

                        send_photo_with_caption(
                            TARGET_CHANNEL, "gerdoo.jpg", caption
                        )
                        send_message(
                            user_chat_id, "✅ تبلیغ گردو با موفقیت در کانال منتشر شد."
                        )

        except Exception as e:
            print("خطای موقت شبکه:", e)
            time.sleep(2)


if __name__ == "__main__":
    main()
