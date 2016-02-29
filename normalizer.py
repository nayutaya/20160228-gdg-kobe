
import re
import mojimoji

class BasicNormalizer:
    def normalize(self, str):
        """
        日本語文字列を正規化する。

        全角の英数字・記号が半角に変換されること。（カタカナは除く）

        >>> normalizer = BasicNormalizer()
        >>> normalizer.normalize('日本語あいうえおアイウエオ')
        '日本語あいうえおアイウエオ'
        >>> normalizer.normalize('０１２３４５６７８９')
        '0123456789'
        >>> normalizer.normalize('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ')
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        >>> normalizer.normalize('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ')
        'abcdefghijklmnopqrstuvwxyz'
        >>> normalizer.normalize('a　！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［¥］＾＿‘｛｜｝〜')
        'a !"#$%&\\'()*+,-./:;<=>?@[\\\\]^_`{|}~'

        改行文字・タブ文字が空白に置換されること。

        >>> normalizer.normalize('a\\tb\\rc\\nd')
        'a b c d'

        連続する空白が圧縮されること。

        >>> normalizer.normalize('a b  c   d')
        'a b c d'

        前後の空白文字が削除されること。

        >>> normalizer.normalize('\\t\\r\\n a\\t\\r\\n ')
        'a'
        """

        str = mojimoji.zen_to_han(str, kana = False)
        str = re.sub('[\t\r\n]', ' ', str)
        str = re.sub(' {2,}', ' ', str)
        str = str.strip()
        return str

if __name__ == "__main__":
    import doctest
    doctest.testmod()
