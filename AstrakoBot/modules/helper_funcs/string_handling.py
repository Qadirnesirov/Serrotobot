import re
import time
from typing import Dict, List

import bleach
import markdown2
import emoji

from telegram import MessageEntity
from telegram.utils.helpers import escape_markdown

# QEYD: url \ escape ikiqat qaçışlara səbəb ola bilər 
# uyğun * (qalın) (url-də olarsa qaçmayın) 
# uyğunluq _ (kursiv) (url-də olarsa qaçmayın) 
# uyğunluq ` (kod) 
# uyğunluq []() (işarələmə linki) 
# başqa, escape *, _, `, və [
MATCH_MD = re.compile(
    r"\*(.*?)\*|"
    r"_(.*?)_|"
    r"`(.*?)`|"
    r"(?<!\\)(\[.*?\])(\(.*?\))|"
    r"(?P<esc>[*_`\[])"
)

# regex to find []() links -> hyperlinks/buttons
LINK_REGEX = re.compile(r"(?<!\\)\[.+?\]\((.*?)\)")
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")


def _selective_escape(to_parse: str) -> str:
    """
    Bütün etibarsız işarələrdən qaçın

    :param to_parse: qaçmaq üçün mətn
    :qayıt: etibarlı işarələmə sətri
    """
    offset = 0 
    # \ simvolunun əlavə edilməsi kimi istifadə ediləcək ofset sətrin sürüşməsinə səbəb olur
    for match in MATCH_MD.finditer(to_parse):
        if match.group("esc"):
            ent_start = match.start()
            to_parse = (
                to_parse[: ent_start + offset] + "\\" + to_parse[ent_start + offset :]
            )
            offset += 1
    return to_parse


# Bu əyləncəlidir.
def _calc_emoji_offset(to_calc) -> int:
    # Bütün emojiləri mətndə əldə edin.
    emoticons = emoji.get_emoji_regexp().finditer(to_calc)
    # Emojinin səbəb olduğu ofseti müəyyən etmək üçün onun utf16 uzunluğunu yoxlayın. 
    # Normal, 1 simvol emoji təsir etmir; buna görə də 1-ci alt. 
    # xüsusi, məsələn, iki emoji simvolu olan (məsələn, üz və dəri rəngi) uzunluğu 2 olacaq, ona görə də birini əlavə etməklə biz 
    # bilirik ki, bir əlavə ofset alacağıq,
    return sum(len(e.group(0).encode("utf-16-le")) // 2 - 1 for e in emoticons)


def markdown_parser(
    txt: str, entities: Dict[MessageEntity, str] = None, offset: int = 0
) -> str:
    """
    Bütün etibarsız markdown obyektlərindən qaçaraq sətri təhlil edin.

    URL-lərin dəyişdirilməsinin qarşısını almaq üçün URL-lərdən qaçır. Müəssisələr obyektindən əldə edilən istənilən teleqram kodu obyektlərini yenidən əlavə edir.

    :param txt: təhlil etmək üçün mətn 
    :param entities: mətndəki mesaj obyektlərinin diktəsi
    :param ofset: mesaj ofset - komanda və qeyd adı uzunluğu 
    :return: etibarlı işarələmə sətri
    """
    if not entities:
        entities = {}
    if not txt:
        return ""

    prev = 0
    res = ""
   # Bütün mesaj obyektləri üzərində dövr edin və: 
   # kodu yenidən daxil edin 
   # müstəqil URL-lərdən qaçın
    for ent, ent_text in entities.items():
        if ent.offset < -offset:
            continue

        start = ent.offset + offset  
        # qurumun başlanğıcı
        end = ent.offset + offset + ent.length - 1  # qurumun sonu

        # Biz yalnız kod, url, mətn bağlantıları ilə maraqlanırıq
        if ent.type in ("code", "url", "text_link"):
            # sayğacı dəyişmək üçün emoji sayın
            count = _calc_emoji_offset(txt[:start])
            start -= count
            end -= count

            # URL-lərin idarə edilməsi -> []() varsa qaçmayın, əks halda qaçın.
            if ent.type == "url":
                if any(
                    match.start(1) <= start and end <= match.end(1)
                    for match in LINK_REGEX.finditer(txt)
                ):
                    continue
                # əks halda, əvvəlki və sonuncu arasındakı qaçışları yoxlayın və sındırmamaq üçün url-dən zorla qaçın
                else:
                    # TODO: çoxlu emoji mövcud olduqda mümkün ofset səhvini araşdırın
                    res += _selective_escape(txt[prev:start] or "") + escape_markdown(
                        ent_text
                    )

            # kodla işləmə
            elif ent.type == "code":
                res += _selective_escape(txt[prev:start]) + "`" + ent_text + "`"

            # markdown/html bağlantılarını idarə edin
            elif ent.type == "text_link":
                res += _selective_escape(txt[prev:start]) + "[{}]({})".format(
                    ent_text, ent.url
                )

            end += 1

        # başqa bir şey
        else:
            continue

        prev = end

    res += _selective_escape(txt[prev:])  
   
    # mətnin qalan hissəsini əlavə edin
    return res


def button_markdown_parser(
    txt: str, entities: Dict[MessageEntity, str] = None, offset: int = 0
) -> (str, List):
    markdown_note = markdown_parser(txt, entities, offset)
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
      
        # btnurl-in qaçıb olmadığını yoxlayın
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # əgər hətta, xilas deyil -> yaratmaq düyməsi
        if n_escapes % 2 == 0:
            # düymə etiketi, url və yeni sətir statusu ilə thruple yaradın
            buttons.append((match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)
        # qəribədirsə, qaçdı -> hərəkət et
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += markdown_note[prev:]

    return note_data, buttons


def escape_invalid_curly_brackets(text: str, valids: List[str]) -> str:
    new_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] == "{":
            if idx + 1 < len(text) and text[idx + 1] == "{":
                idx += 2
                new_text += "{{{{"
                continue
            else:
                success = False
                for v in valids:
                    if text[idx:].startswith("{" + v + "}"):
                        success = True
                        break
                if success:
                    new_text += text[idx : idx + len(v) + 2]
                    idx += len(v) + 2
                    continue
                else:
                    new_text += "{{"

        elif text[idx] == "}":
            if idx + 1 < len(text) and text[idx + 1] == "}":
                idx += 2
                new_text += "}}}}"
                continue
            else:
                new_text += "}}"

        else:
            new_text += text[idx]
        idx += 1

    return new_text


SMART_OPEN = "“"
SMART_CLOSE = "”"
START_CHAR = ("'", '"', SMART_OPEN)


def split_quotes(text: str) -> List:
    if not any(text.startswith(char) for char in START_CHAR):
        return text.split(None, 1)
    counter = 1  # ignore first char -> is some kind of quote
    while counter < len(text):
        if text[counter] == "\\":
            counter += 1
        elif text[counter] == text[0] or (
            text[0] == SMART_OPEN and text[counter] == SMART_CLOSE
        ):
            break
        counter += 1
    else:
        return text.split(None, 1)

    # Başlanğıc sitatın qarşısını almaq üçün 1 və sayğac eksklüzivdir, buna görə də bitmənin qarşısını alır
    key = remove_escapes(text[1:counter].strip())
    # indeks diapazonda olacaq və ya `başqa` yerinə yetirilib qaytarılacaqdı
    rest = text[counter + 1 :].strip()
    if not key:
        key = text[0] + text[0]
    return list(filter(None, [key, rest]))


def remove_escapes(text: str) -> str:
    res = ""
    is_escaped = False
    for counter in range(len(text)):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
    return res


def escape_chars(text: str, to_escape: List[str]) -> str:
    to_escape.append("\\")
    new_text = ""
    for x in text:
        if x in to_escape:
            new_text += "\\"
        new_text += x
    return new_text


def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            message.reply_text("Yanlış vaxt məbləği göstərildi.")
            return ""

        if unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "d":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            # how even...?
            return ""
        return bantime
    else:
        message.reply_text(
            "Yanlış vaxt növü göstərildi. Gözlənilən m,h və ya d, alındı: {}".format(
                time_val[-1]
            )
        )
        return ""


def markdown_to_html(text):
    text = text.replace("*", "**")
    text = text.replace("`", "```")
    text = text.replace("~", "~~")
    _html = markdown2.markdown(text, extras=["strike", "underline"])
    return bleach.clean(
        _html, tags=["strong", "em", "a", "code", "pre", "strike", "u"], strip=True
    )[:-1]
