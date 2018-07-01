// function() 包裹在$()中，表示整个网页都加载完毕之后才会执行function中的代码
// 🌟 模态对话框保存按钮
$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        // 先获取模态对话框的元素，效率更高
        var self = $(this);
        var dialog = $('#banner-dialog');
        var nameInput = $("input[name='name']");
        var imageInput = $("input[name='image_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");

        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();

        // 将data-type属性绑定到'保存'按钮上面：意思是提交的类型
        var submitType = self.attr('data-type');
        var bannerId = self.attr('data-id');

        // 判断是否输入完整
        if (!name || !image_url || !link_url || !priority) {
            zlalert.alertInfoToast("请输入完整的轮播图数据！");
            return;
        }

        // 如果提交类型是更新类型
        if (submitType == 'update') {
            url = '/cms/ubanner/'
        } else {
            url = '/cms/abanner/'
        }
        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                // 隐藏模态对话框
                dialog.modal("hide");
                if (data['code'] == 200) {
                    zlalert.alertInfoToast('保存成功！');
                    //重新加载当前页面
                    window.location.reload();
                } else {
                    zlalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        })
    })
});

// 🌟 模态对话框：编辑按钮
$(function () {
    $(".edit-banner-btn").click(function (event) {
        // 0. 拿到当前对象，就是这个edit-banner-btn按钮
        var self = $(this);
        event.preventDefault();
        // 1. 找到模态对话框
        var dialog = $('#banner-dialog');

        // 2. 显示模态对话框
        dialog.modal('show');

        // 3. 通过edit-banner-btn这个button标签的父级的父级获取到tr标签
        var tr = self.parent().parent();

        // 4. 获取相关数据，从tr标签的属性中取值
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        // 5. 取各个标签
        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        // 6. 将获取到的数值复制给当前的各个标签
        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);

        // 7. 给编辑中的保存按钮绑定一个属性：data-type,属性的值为update
        // 意思是：点击了编辑之后，才绑定这个属性，说明是编辑界面的'保存'按钮
        saveBtn.attr("data-type", "update");
        saveBtn.attr("data-id", tr.attr('data-id'));

    })
});


$(function () {
    $('.delete-banner-btn').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        //1. 拿到banner_id
        var banner_id = tr.attr('data-id');
        event.preventDefault();

        //2. 弹出框
        zlalert.alertConfirm({
            'msg': '您确定要删除这个轮播图吗?',
            // 确认删除 - 回调函数
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dbanner/',
                    'data': {
                        'banner_id': banner_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            zlalert.alertInfoToast('删除成功！');
                            //重新加载当前页面
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        })
    })
});
















