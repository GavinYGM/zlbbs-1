$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();

        // 1. 获取新邮箱的元素
        var newmailE = $("input[name=email]");

        // 2. 获取新邮箱元素的值
        var newmail = newmailE.val();

        // 2.1 ajax请求提交表单
        zlajax.post({
            'url': '/cms/resetemail',
            'data': {
                'newmail': newmail
            },
            'success': function (data){
                if(data['code'] == 200){
                    
                }
            }
        })

    })
})