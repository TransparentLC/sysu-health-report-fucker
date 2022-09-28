browser.webRequest.onBeforeRequest.addListener(
    () => ({cancel: true}),
    {
        urls: [
            '*://cas.sysu.edu.cn/favicon.ico',
            '*://cas.sysu.edu.cn/cas/css/bootstrap.min.css*',
            '*://cas.sysu.edu.cn/cas/css/font-awesome.min.css*',
            '*://cas.sysu.edu.cn/cas/images/caslogo.png',
            '*://cas.sysu.edu.cn/cas/js/bootstrap.min.js*',
            '*://cas.sysu.edu.cn/cas/js/gt.js*',
            '*://cas.sysu.edu.cn/cas/js/head.min.js*',
            '*://cas.sysu.edu.cn/cas/js/jquery.min.js*',
            '*://cas.sysu.edu.cn/cas/js/jquery.cookie.min.js*',
            '*://cas.sysu.edu.cn/cas/js/jquery-ui.min.js*',
            '*://cas.sysu.edu.cn/cas/js/wxLogin.js*',
            '*://cas.sysu.edu.cn/cas/js/zxcvbn.js*',
            '*://cas.sysu.edu.cn/cas/themes/sysu2-bottom/css/cas.css*',
            '*://cas.sysu.edu.cn/cas/themes/sysu2-bottom/images/bodybg.jpg',
            '*://cas.sysu.edu.cn/cas/themes/sysu2-bottom/js/cas.js*',
            '*://jksb.sysu.edu.cn/infoplus/static/css/infoplus.css*',
            '*://jksb.sysu.edu.cn/infoplus/static/css/fonts/icomoon.ttf*',
            '*://jksb.sysu.edu.cn/infoplus/static/img/*.png',
            '*://jksb.sysu.edu.cn/infoplus/static/themes/default/desktop/css/theme.css*',
            '*://open.weixin.qq.com/*',
            '*://res.wx.qq.com/*',
        ],
    },
    ['blocking'],
);