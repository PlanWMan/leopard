import re
import execjs


def get_y9r(indexs):
    jscontent = """
        function M(m, P) {
        var D = 2;
        while (D !== 10) {
            switch (D) {
            case 13:
                d -= 1;
                D = 6;
                break;
            case 8:
                D = R < m ? 7 : 11;
                break;
            case 7:
                var d = m - 1;
                D = 6;
                break;
            case 1:
                var l = 0;
                D = 5;
                break;
            case 3:
                l += 1;
                D = 5;
                break;
            case 11:
                return J;
                D = 10;
                break;
            case 14:
                J[R][(d + P * R) % m] = J[d];
                D = 13;
                break;
            case 9:
                var R = 0;
                D = 8;
                break;
            case 6:
                D = d >= 0 ? 14 : 12;
                break;
            case 4:
                J[(l + P) % m] = [];
                D = 3;
                break;
            case 2:
                var J = [];
                D = 1;
                break;
            case 5:
                D = l < m ? 4 : 9;
                break;
            case 12:
                R += 1;
                D = 8;
                break;
            }
        }
    };


    function get_y9r(indexs){
        var H = M(48, 14);
        var temp = H;
        for (i = 0; i < indexs.length; i++) {
            temp = temp[indexs[i]];

        }
        // console.log(H.indexOf(temp));
        return H.indexOf(temp);
    };


    var H = M(48, 14);
        // lists = H;
    console.log(H.indexOf(H[31][29][21][21]));

    // console.log(get_y9r([7,28,6]));
    """
    # with open('y9r.js','r+',encoding='utf8') as f:
    #     jscontent = f.read()
    ctx = execjs.compile(jscontent)
    results = ctx.call("get_y9r", indexs)
    # print(ctx.call("get_y9r",[7,28,16]))
    return int(results)


def replace_y9r():
    content = ''
    replace_lists = []

    # 按行读取./qixin_2.js文件
    with open('./qixin_2.js', 'r+', encoding='utf8') as f:
        content = f.readlines()

    # 按行处理,形成要替换的如'B2BB.k9r()[13][17][21]'和对应值的对照关系列表
    for con in content:
        temp = re.findall(r'(B2BB.(L9r|k9r)\(\)(\[\d+\])+)', con)
        if temp:
            # temp = [('B2BB.k9r()[13][17][21]', 'k9r', '[21]')] 
            for (b2bb, lrkr, num) in temp:
                indexs = list(map(lambda x: int(x), re.findall(r'\[(\d+)\]', b2bb)))
                # indexs = [13, 17, 21]
                y9r = get_y9r(indexs)
                # y9r = 27
                replace_lists.append((b2bb, y9r))

    # 对结果列表按照待替换字符串(如'B2BB.k9r()[13][17][21]')的长度进行降序排序
    # 不排序则可能会导致B2BB.k9r()[13][17][21][20]的值呗B2BB.k9r()[13][17][21]替换掉
    replace_lists = sorted(replace_lists, key=lambda x: len(x[0]), reverse=True)

    # 读取./qixin_2.js文件内容，准备替换字符串
    with open('./qixin_2.js', 'r+', encoding='utf8') as f:
        content = f.read()

    # 替换字符串和对应的值
    for (b2bb, y9r) in replace_lists:
        content = content.replace(b2bb, str(y9r))

    # 将替换后内容写入文本./qixin_3.js
    with open('./qixin_3.js', 'w+', encoding='utf8') as f:
        f.write(content)


def replace_z8z():
    # 运行js ，拿到M的值
    M = ["fullbg", "create", "bb", "show", "homepage", "attachEvent", "s", "geetest_style_detect_178273px",
         "a.gt_refresh_button", "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqr", "MSPointerDown",
         "onStatusChange", "random", "fb", "ボタンを終点までドラックしてください", "sec 秒的速度超過 score% 的用戶", ".gt_refresh_button",
         "178273px", "pictures", "gt_custom_error", "fromString", "10001",
         "00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81",
         "parse", "querySelector", "x", "substring", "$super", "evts", "pb", "Ob", "b2", "La", "Abuse", "滑動至此完成驗證",
         "&callback=", "domSelectorError", "인증실패", "userAgent", "DomEvent", "length", "onerror",
         "http://www.geetest.com/first_page", "geetest_validate", "xpos", "crossOrigin", "Oa", "round", "unload",
         "画像が更新されています", "onreadystatechange", "Input", "Data", "nextBytes", "/static/",
         "สำเร็จ ความเร็ว sec วินาที เร็วมากๆ", "getRandomValues", "Try Again:", "/gt-dist/local", "ya",
         "progid:DXImageTransform.Microsoft.AlphaImageLoader(src=\"", "Ya", "gb", "left", "Geetest", "upHandler",
         "algo", "DB", "putImageData", "Success:", "Arr", "Nb", "onGeetestLoaded", "javascript:;", "top",
         "Take secs and defeat score% users", "?", "lock", "mod", "กดและลากเพื่อประกอบภาพ", "zh", "zh-CN", "blur",
         ".gt_curtain_bg_wrap", "y", "\"", "apply", ".gt_loading_text", ".gt_holder_top", "mousedown",
         " can not access", "3.2.0", "Ub", "DV", "fromInt", "isEven", "ub", "multiplyTo", "Tip", "刷新验证", "cy", "popup",
         "imgload", "replace", "gt_show", "stringify", ".gt_refresh_tips", ".gt_popup_finish", "changedTouches",
         "theme_version", "r", "Pa", "input.geetest_validate", "copyTo", "touchcancel", "Qa", "M", "popup_btn", "Na",
         "出现错误:", "v6.0.9 Geetest Inc.", ".gt_popup_ready", "protocol", "mode", "addEventListener", "hb", "hoverChange",
         "Vb", "split", "驗證通過:", ".gt_box_holder", "fEkexGxOwUyY", "endTime", "msTransition", "canvas", "Base",
         "show_delay", "传参错误:", "none", "number", "o", "coeff", "幫助", "all",
         "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()", "forbidden", "SvgError", "Benchmark",
         "fromNumber", "Forbidden", "curtain", "b1", "Ab", "尝试过多:", "請先完成下方驗證", "/js", "destroy",
         "Microsoft Internet Explorer", "serial", "offsetTop", "cx", "curtain_knob", "コメント", "getElementsByTagName",
         "null", "className", "getPasstime", "ta", "autoRefresh", "charAt", "\"", "!", "Gyro", "zh-tw", "]",
         "webkitTransition", "Qb", "확인하기 위해 여기로 이동", "Wow~ Monster eats the image", "innerText", "/gt-dist",
         "drShiftTo", "e", "loading...", "回報問題", "toFixed", "count秒後もう一度やり直してください", ".webp", "帮助反馈", "gt", "d", "async",
         "小怪物吃掉了拼圖 count 秒後重試", "passtime", "contains", "h", "enable", "もう一度やり直してください", "toString", "once", "Flow",
         "value", "GeeTest Error: request ", "onload", "startTime", "negate", ".gt_popup_cross", "nextSibling",
         ".gt_guide_tip", "UTF-8", "va", "กดค้างและลากเพื่อต่อภาพให้สมบูรณ์", "更新驗證圖", "2d", "abs", " lost!", "qa",
         "success", "apiserver", "Sa", "drawImage", "important", "enc", "", "parallel", ".gt_slider", "stylesheet",
         "loading", "Pkcs7", "help", "hasOwnProperty", "Base64", "modPowInt", "接口", "按住左邊滑塊，拖動完成上方拼圖", "CipherParams",
         "验证失败:", "gt_clean", "系统正在自动刷新图片", "createElement", "กรุณารอสักครู่", ".gt_curtain_button",
         "Drag the left slider to verify", "sigBytes", ".gt_input", "scroll", "img", "touchstart", "Browser",
         "0000000000000000", "svg ", "_https", "Event", "A", "You will be redirected in 2 seconds", "styleDetectEle",
         ".gt_flash", ".gt_box", "content", "MSPointerUp", "Ha", ".gt_slider_knob", "blockSize", "//", "FV", ".js",
         "Ka", "getModule", ".jpg", "encryptBlock", "WordArray", "BufferedBlockAlgorithm", "Excessive:", "kb",
         "processBlock", "J", "Aa", "jQuery", "refresh error", "點擊上圖並沿路線滑至終點", "onmousemove", ",", "fromCharCode",
         "static.geetest.com", "default", "gt_ajax_tip gt_", "finalize", "/static/js/", "もう一度:", "self",
         "按住左边滑块，拖动完成上方拼图", "error", ".gt_info_icon", "q", "paddingBottom", "불러오는 중...", "I", "}", "offline", "Loaded",
         "squareTo", "filter", "invDigit", "다음 인증을 완성하세요", "exp", "panelHeight", "statusChange", "global",
         "debugConfig", "Message too long for RSA", "reset", "eb", "gt_info_content", "hidden", "preventDefault", "_",
         "gt_info_tip gt_", "Utility", " gt_clone", "sec", "log", ".gt_curtain", "lang", "/pictures/gt/", "Pb", "za",
         "width", "no such resource: ", "type", "indexOf", "Success", "gt_hide", "mb", "backgroundImage",
         ".gt_info_text", "rp", "cb", "local_path", "驗證失敗:", "onRefresh", "push", "a.gt_box_tips", "message", "lib",
         "ログイン認証を行ってください", "-cn", "", "cloneDom", "載入中...", "setAttribute", "SVG", "i", "onSuccess", "系統正在更新圖片",
         ".gt_logo_button", "WebPLoaded", "stuvwxyz~", "undefined", "object", "Cipher", "count", ".", "bitLength",
         "Encryptor", "next", "lb", "xb", "Cb", "页面将在2秒后跳转", ".gt_curtain_tip", "!!", ".gt_cut_bg", ".gt_cut_curtain",
         "getBoundingClientRect", "can not loaded imgs", "-tw", "Y", "2秒後でリダイレクトします", "g", "retry", "click", "height",
         "max", "反馈", "B", "ypos", "กำลังดาวน์โหลด...", "module ", "pad", "a.gt_bg", "callback", "getComputedStyle",
         "refresh", ".gt_loading", ".gt_help_tips", "Netscape", "inline-block", "deviceorientation", "use strict",
         "http://", "hideDelay", "document", "$", "wa", "margin-left", "6_11_7_10_4_12_3_1_0_5_2_9_8", "F1", "floor",
         "Jb", "loaded_theme", "กรุณาปิดและเปิดใหม่อีกครั้ง", "slide", ".gt_bg", "https://", "REFb0UEJ", "prototype",
         "crypto", "gt_holder gt_", "yb", "divRemTo", "pointermove", "p", "Wa", "referer_encode", "compareTo",
         "challenge", ".geetest_validate", "エラーです:", "words", "define", "Info", "Fullpage", "a.gt_curtain", "doPublic",
         "onAbuse", ".gt_mask", "Db", "pointerdown", ".geetest_seccode", "S", "visible", ".css", "_a", "style",
         "geetest_seccode", "getImageData", "点击上图按钮并沿道路拖动到终点处", "clamp", "splice", "Utf8", ".gt_cut_fullbg", "zh-cn",
         "/refresh.php", "Ma", "버튼 드리그하여 인증하세요", "a.gt_help_button", ".gt_curtain_bg", "DM", "charCodeAt", "startY",
         "移动到此开始验证", "Ta", "setFloat", "$a", "ONE", "|", "hide_delay", "input.geetest_seccode", "touchend", "on",
         "onError", "id", "\":", "Ba", "Please try again later", "clientX", "gtError", "substr", "cursor", "move",
         "getLang", "call",
         "data:image/webp;base64,UklGRi4AAABXRUJQVlA4TCEAAAAvAUAAEB8wAiMwAgSSNtse/cXjxyCCmrYNWPwmHRH9jwMA", "Latin1",
         "zb", "product", "removeAttribute", "moveHandler", "childNodes", "convert", "BlockCipher", "getContext", "vb",
         "gt_moving", "bg", "benchmark", "pointerup", "ib", "Xa", "mpl", "hideRefresh", "Ra", "srcElement", "ab",
         "slice", "gt_holder gt_mobile_holder gt_", "_blank", "불러오는 중", "a.gt_logo_button", "staticservers", "ล้มเหลว:",
         "db", "subTo", "concat", "MSPointerMove", "exports", "getValidate", "読み込み中…", "Ga", "a.gt_fullbg", "script",
         "offsetParent", "removeChild", "boolean", "拖动滑块将悬浮图像正确拼合", "static_servers", "再来一次:", "padding", "0",
         "|jordan", "gt_no_logo", "geetest_challenge", "hk", "Offline", "md5", "scale", "Invalid RSA public key", ")",
         "name", "อุ๊ย! ต่อภาพไม่ถูกต้องกรุณาลองใหม่", "c", "eles", ".gt_ajax_tip", "input", "u", "Ja", "/style",
         "BlockCipherMode", "Ea", "function", "onForbidden", "Eb", "detachEvent", "theme", "갱신", "link", "Global",
         "gt_cut_", "Unsuccessful:", "button", "offsetLeft", "charset", "Geetest requires a window with a document",
         "complete", "dn-staticdown.qbox.me", "길을 따라 버튼을 드래그", " ", "Refresh", ".gt_widget", ".gt_popup_wrap", "cfg",
         "onFail", "appendTo", "Modules", "pow", "jb", "shell", "outerHTML", "init", "gt_custom_ajax", "startX", "in",
         ".gt_bottom", "float", "Decoder", "setProperty", "am", "gt_custom_refresh", "ms-touch-action", "toRadix",
         "gJSON", "iy", "join", "加载中...", "Ia", "1234567890.", "extend", "px ", "認証が完了しました", "appName", "callbackError",
         "ajax", "b", "{", "/static", "tb", "noConflict", "auto", "スライドして認証を完成させてください", "fail", "down", "ready",
         "rShiftTo", "mt2", "body", "Complete the puzzles", "N", "removeEventListener", "lShiftTo", "_slice", "รีเฟรช",
         "xa", "api_server", "fFtZ0VaY4Gg.", "geetest_", "reduce", "请先完成下方验证", "n", "Rb", "gt_animate", "status", "mph",
         "認証完了:", "260px", "na", "touch-action", "parentNode", "getElementById", "验证通过:", "mouseup", "createTextNode",
         "logo", "/skin.", "feedback", "https", "ระบบกำลังดำเนินการเปลี่ยนภาพใหม่", "Slide", ".geetest_challenge",
         "Request", "input.geetest_challenge", "abuse", "dmq1", ".svg", "Va", "0123456789abcdefghijklmnopqrstuvwxyz",
         "overflow", "画像更新", "Gb", "dmp1", "DOMReady", "gyroscope", "target", "popup_ready", "span", "Curtain",
         ".gt_help_button", "AES", "sb", "rel", "頁面將在2秒後跳轉", "sqrTo", "loaded", "자동재행 중", "Complete verification below",
         "ELEMENT_NODE", "Fail", "j", "isArray", "Analyse", "gt_info_type", "readyState", "Dom",
         "Server is refreshing the image", "ix", "http://www.geetest.com/contact#report", "webp", "clientWidth",
         "Support", "event", "Ua", "validate", "hide", "popup_copy_btn", "div", "Bb", "up", "revert", "test",
         "toLowerCase", "encrypt", "&", "innerHTML", "api.geetest.com", "url(", "m", "인증성공", "handlerList", ".png",
         "哇哦～怪物吃了拼图 count 秒后重试", "zoom", "ob", "請將懸浮圖片拼合", "currentStyle", "fullpage", "mousemove", "mozTransition",
         "clean", "ciphertext", "dom", "請關閉驗證後重試", "returnValue", "insertBefore", "C", "Mb", "compareDocumentPosition",
         "popupbtnid", "sa", "score", "Za", "F2", "getPropertyValue", "CBC", "cloneNode", "fromRadix", "transition",
         "bindOn", "origin_", "popup_finish", "valueOf", "ヘルプ", "Sb", "end", "Feedback", "再來一次:", "認証失敗:", "res",
         "ここから認証を始めます", "mulTo", "getTime", "请关闭验证重试", ".gt_info", "qb", ".gt_popup_header", " skin.js can not loaded",
         "Fa", "パズルを合わせてください", ".gt_popup_box", "6.0.9", "infoHide", "touchmove", "Animate", "Move here to verify",
         "Drag the button along the road", "=", "arr", "disable", " can not loaded", "tw", ".gt_slice", "iv", "moving",
         "Tool", "dlShiftTo", "Server Error:", "format", ".gt_fullbg", ".gt_loading_icon", "/", "mixIn", "t", "string",
         "a", ".gt_cut_", ".gt_box_tips", "focus", ".gt_ie_success", "l", "min", "Popup", "nodeType", "-", "Ib", "rb",
         "backgroundPosition", "[", "px", ".gt_info_tip", "golden", "ช่วยเหลือ", "enablePopup", "문의", "[object Array]",
         "SerializableCipher", "sec 秒的速度超过 score% 的用户", "#", "mobile", "createEncryptor", "Fb", "display",
         "appendChild", "setPublic", "ceil", "mp", "Anonymous", "href", "ZERO", "กรุณาดำเนินการตรวจสอบด้านล่าง",
         "mobileSkins", "wb", "onReady", "GeeTestSkins", "clientY", ".gt_curtain_knob", "Lb", "sandbox", "um",
         "version", "\")", "src", "出現錯誤:", "Kb", "다시 시도하세요", "head", "Da", "嘗試過多次:"]

    content = ''
    # 以./qixin_1.js(该文件内容已经处理过十六进制字符串)为基础进行替换
    with open('./qixin_1.js', 'r+', encoding='utf8') as f:
        content = f.read()

    # 利用整理匹配出需要替换的地方，并替换成M对应索引的值
    c8z = re.findall(r'(M9r\.C8z\((\d+?)\))', content)
    for (name, num) in c8z:
        content = content.replace(name, '"' + M[int(num)] + '"')

    r8z = re.findall(r'(M9r\.R8z\((\d+?)\))', content)

    for (name, num) in r8z:
        content = content.replace(name, '"' + M[int(num)] + '"')

    for (name, num) in re.findall(r'(T9r\.C8z\((\d+?)\))', content):
        content = content.replace(name, '"' + M[int(num)] + '"')

    for (name, num) in re.findall(r'(T9r\.R8z\((\d+?)\))', content):
        content = content.replace(name, '"' + M[int(num)] + '"')

    # js中 var T9r = B2BB;,则把T9r.替换成B2BB. 方便进行下一步数据处理
    if 'T9r.' in content and 'var T9r = B2BB;' in content:
        content = content.replace('T9r.', 'B2BB.')

    # js中 var M9r = B2BB;,则把M9r.替换成B2BB. 方便进行下一步数据处理
    if 'M9r.' in content and 'var M9r = B2BB;' in content:
        content = content.replace('M9r.', 'B2BB.')

    # 将处理后的js内容，记录在./qixin_2.js中
    with open('./qixin_2.js', 'w+', encoding='utf8') as f:
        f.write(content)
    # print (c8z)


def parse16():
    content = ''

    with open('./qixin.js', 'r+', encoding='utf8') as f:
        content = f.read()
        pattern = re.compile(r'\\x[a-zA-Z0-9]{2}')
        for i in pattern.findall(content):
            content = content.replace(i, i.encode('utf-8').decode('unicode_escape'))
    print(content)
    with open('./qixin_1.js', 'w+', encoding='utf8') as f:
        f.write(content)


def main():
    replace_z8z()
    # parse16()
    parse16()
    # get_M()
    replace_y9r()
    # print(get_y9r([21,33,21]))
    # replace_y9r()


if __name__ == '__main__':
    main()
