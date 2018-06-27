// 图片验证码
$(function () {
    $('#captcha-img').click(function () {
        // 1. 将js原生对象转换成jquery对象
        var self = $(this);

        // 2. 获取img标签上面的src属性，拿到了src
        var src = self.attr('src');

        // 3. 利用zlparam设置新的src,重新加载整个页面
        // src标签的内容改变，img标签会自动加载（等同于刷新了页面）
        // 后台查询字符串 /catpcha/?xx=1.234123564523这种形式
        var newsrc = zlparam.setParam(src, 'xx', Math.random());

        // 4. 给src设置属性newsrc
        self.attr('src', newsrc);
    });
});

// 短信验证码
$(function () {
    $('#sms-captcha-btn').click(function (event) {
            // 1. 在表单中，如果有一个button按钮，他的默认行为是：
            // 点击这个按钮之后，会提交所有的表单数据，所以这里我们要阻止他的默认行为
            event.preventDefault();

            // 将按钮对象变成jqueyr对象，现在self对象就代表这个按钮
            var self = $(this);

            // 2. 拿到手机号码
            var telephone = $('input[name="telephone"]').val();

            // 3. 判断手机号是否填写正确
            if (!(/^1[345879]\d{9}$/.test(telephone))) {
                zlalert.alertInfoToast('请输入正确的手机号码！');
                return;
            }

            // 获取时间戳
            var timestammp = (new Date).getTime();
            // 获取签名
            var sign = md5(timestammp + telephone + 'qewr234234werjk;adsfkd;sfka');
            zlajax.post({
                // 'url': '/c/sms_captcha?telephone=' + telephone,
                'url': '/c/sms_captcha/',
                'data': {
                    'telephone': telephone,
                    'timestamp': timestammp,
                    'sign': sign
                },
                'success': function (data) {
                    // console.log(data);
                    if (data['code'] == 200) {
                        zlalert.alertSuccessToast('短信验证码发送成功');
                        // 现在this代表字典对象
                        //this.

                        // 给按钮添加disable属性
                        self.attr("disabled", 'disabled');

                        // jquery重的倒计时,第一个参数是倒计时执行的函数，第二个参数是每个多少毫秒执行
                        var timeCount = 60; // 设置初始时间
                        // setInterval函数一旦执行就会返回这个timer变量(对象)
                        // 清除倒计时的时候，就调用这个对象
                        var timer = setInterval(function () {
                            timeCount--;
                            self.text(timeCount); // 设置这个按钮的文本内容
                            // 当倒计时结束时：，清除disabled属性
                            if (timeCount <= 0) {
                                self.removeAttr('disabled');
                                // 停止倒计时事件
                                clearInterval(timer);
                                // 变回原来的发送验证码
                                self.text('发送验证码');
                            }
                        }, 1000)
                    } else {
                        zlalert.alertInfoToast(data['message']);
                    }
                },
                'fail': function (data) {
                    console.log(data);
                }
            });
        }
    )
});

$(function () {
    $('#submit-btn').click(function () {
        // 0. 阻止默认事件，如果不阻止，点击button按钮，会自动将表单提交
        event.preventDefault();

        // 1. 获取输入框各种标签
        // 手机号码
        var telephone_input = $("input[name='telephone']");
        // 短信验证码
        var sms_captcha_input = $("input[name='sms_captcha']");
        //用户名
        var username_input = $("input[name='username']");
        //密码
        var password1_input = $("input[name='password1']");
        //确认密码
        var password2_input = $("input[name='password2']");
        //图形验证码
        var graph_captcha_input = $("input[name='graph_captcha']");

        // 2. 获取各输入框的值
        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        // ajax请求
        zlajax.post({
            'url': '/signup/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'username': username,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            // 请求成功200的时候
            'success': function (data) {
                if (data['code'] == 200) {
                    // 跳转到首页
                    window.location = '/'
                } else {
                    // zlalert.alertInfo(data['message']);
                    zlalert.alertInfo('注册失败！')
                }
            },
            // 404 500等错误
            'fail': function () {
                zlalert.alertNetworkError();
            }
        })
    })
});