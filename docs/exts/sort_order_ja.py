#
# -*- encoding: utf-8 -*-

"""
    sort_order_ja
    ~~~~~~~~~~~~~

    The Sphinx extension to provide sort order for typical Japanese.

    :copyright: (c) 2011 by Suzumizaki-Kimitaka.
    :license: 2-clause BSD.
"""

"""Japanese specific SortOrderBase definitions

To use one of follows you can choice:
#. if you set the config 'language' to 'ja',
   you don't have to do anything.
#. add 'sort_order_jp' to the list of config 'ext'.

Of course, any directives or modules need sorting
must import sort_order module, like 'yogosyu' and
'user_ordered_index_patch' do.

日本語用の SortOrderBase 実装です。
各ディレクティブなどが sort_order を import して
活用しないことには当然効果が出ません。
yogozyu と user_ordered_index_patch の両方を 'ext' で
指定する必要があります。

conf.py で language = 'ja' を指定しておけば何もしなくても
必要な拡張から読み込まれるようになっています。
そうでない場合は ext の拡張リストの中に 'sort_order_ja' を
含めることで自動的に SortOrderJa が使われるようになります。

今のところディレクティブ yogosyu で読み仮名を与えることになります。
読み仮名、と言ってますが別にひらがなやカタカナだけで書かなくても
構いません。索引を目で探すことを考えて設定してください。例えば、
英単語に対してカタカナを当てることにはあまり意味がありません。
単語の一部が英語になっている場合、ルビとは異なり読み仮名も英語の
ままにしておくほうが良いように思います。

並べ替えは次の順序になります:
#. 小書きの文字は通常文字の直後
#. 濁音は対応する清音の直後
#. 半濁音は対応する濁音の直後
#. ASCII内の英字はかなの後ろ
#. 大文字小文字・ひらがなカタカナは区別しない
#. 一方が他方を包含する場合は短い方が先
#. genindexの索引においてはかな→英字→その他の順
#. 長音は適切であれば「あいうえおん」のどれかに置換。

conf.py 用にいろいろ定義して細かく制御もできそうですが、
それは今後の課題、あるいは皆さんでご自由に。
"""

import sort_order
import string

ord_hiragana_begins = 0x3041
ord_hiragana_vu = 0x3094
ord_hiragana_ends = 0x3097
ord_katakana_begins = 0x30a1
ord_katakana_vu = 0x30f4

diff_katakana_hiragana = ord_katakana_begins - ord_hiragana_begins

def hiragana_to_katakana(s):
    """Translate Katakana in s to Hiragana

    I don't know why we can't use s.translate and string.maketrans
    in this case.
    """
    r = u''
    for c in s:
        if ord_hiragana_begins <= ord(c) <= ord_hiragana_vu:
            r += unichr(ord(c) + diff_katakana_hiragana)
        else:
            r += c
    return r

vowels_for_tyoon = (
    u'アァカヵガタダナハバパマヤャラワヮヷ',
    u'イィキギシジチヂニヒビピミリヰヸ',
    u'ウヴゥクグスズツッヅヌフブプムユュル', 
    u'エェケヶゲセゼテデネヘベペメレヱヹ',
    u'オォコゴソゾトドノホボポモヨョロヲヺ',
    u'ン',
    )

def tyoon_to_vowel(s):
    """Translate prolong mark to suit vowel Katakana

    @param s whole string
    @return tranlated s

    直前の文字を元に長音符号を母音に直して返す趣旨。
    """
    r = u''
    for c in s:
        if c != u'ー' or not len(r):
            r += c
            continue
        prev = r[-1]
        for l in vowels_for_tyoon:
            if prev in l:
                r += l[0]
                break
        else:
            r += c
    return r    

kana_need_insert_after = {
    u'ウ': u'ヴ',
    u'カ': u'ヵ',
    u'ケ': u'ヶ',
    u'ワ': u'ヷ',
    u'ヰ': u'ヸ',
    u'ヱ': u'ヹ',
    u'ヲ': u'ヺ',
    }
sutegana_katakana_swappable = u'ァィゥェォッャュョヮ'
katakana_swappable_with = u'アイウエオツヤユヨワ'
kana_reorder = u''
for k in range(ord_katakana_begins, ord_katakana_vu):
    kc = unichr(k)
    idx = katakana_swappable_with.find(kc)
    if idx >= 0:
        ks = sutegana_katakana_swappable[idx]
        kana_reorder = kana_reorder[:-1] + kc + kana_reorder[-1]
    else:
        kana_reorder += kc
    if kc in kana_need_insert_after:
        kana_reorder += kana_need_insert_after[kc]        
headings = {
    kana_reorder[:11]: u"あ",
    kana_reorder[11:23]: u"か",
    kana_reorder[23:33]: u"さ",
    kana_reorder[33:44]: u"た",
    kana_reorder[44:49]: u"な",
    kana_reorder[49:64]: u"は",
    kana_reorder[64:69]: u"ま",
    kana_reorder[69:75]: u"や",
    kana_reorder[75:80]: u"ら",
    kana_reorder[80:90]: u"わ",
    }
assert len(kana_reorder) == 90
assert kana_reorder[75:80] == u'ラリルレロ'


class SortOrderJa(sort_order.SortOrderBase):
    """Japanese specific SortOrder implementation

    This class requires Yomigana the string to sort instead of
    binded the term itself.
    """

    def get_string_to_sort(self, entry_name):
        """Return the string to sort instead of given yomigana

        @param entry_name the term itself or converted yomigana
        @return the string to sort
        """
        s = self.get_ja_canonical_yomi(entry_name)
        r = u''
        for c in s:
            idx = kana_reorder.find(c)
            if idx >= 0:
                r += unichr(ord_hiragana_begins + idx)
            else:
                r += c
        if r[0] in string.ascii_letters:
            return u'\ufffd' + r.lower()
        return r.lower()

    def get_group_name(self, entry_name):
        """Return the group name of the given entry

        @param entry_name the term itself or converted yomigana
        @return the string to sort
        
        英字は文字通り英字しかグループ化しないのでそのあたりは
        get_string_to_sort() ともども改善の余地有り。
        """
        s = self.get_ja_canonical_yomi(entry_name)
        if s[0] in string.ascii_letters:
            return u'英字'
        for k,v in headings.iteritems():
            if s[0] in k:
                return v
        return u"その他"

    def get_ja_canonical_yomi(self, entry_name):
        """与えられた名前の読みを返す

        このクラス専用の内部関数。
        実際には読みを得た上でひらがなをカタカナにし、長音も母音化した
        文字列を返す。
        """
        n = hiragana_to_katakana(entry_name)
        n = tyoon_to_vowel(n)
        return n


def get_default_sort_order(cfg):
    """Return vaild sort order as default in this module

    Called by the function that has same name
    in sort_order.py.
    """
    return SortOrderJa()


def setup(app):
    """Extends Sphinx as we want

    @param app sphinx.application.Sphinx object to use add builder or so.
    """
    sort_order.setup(app)
    app.add_config_value('sort_order', SortOrderJa(), 'env')
    return

