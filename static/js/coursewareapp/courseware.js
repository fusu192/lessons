$(function () {
    $(".courseware-name a").click(function () {
        var courseware_id = $(this).children("input[name='courseware-id']").val();
        $.ajax({
            url: "/courseware/downloadnums/",
            type: "post",
            data: {
                "courseware-id": courseware_id,
                "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                if (data["status"] == true) {
                    console.log("下载成功!")
                } else {
                    console.log("下载失败!")
                }
            }
        })
    });

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
            }
        }
    });
    $(".delete-courseware").click(function () {
        var mymessage = confirm("确认删除课件？");
        if (mymessage == true) {
            var delete_obj = $(this);
            $.ajax({
                url: "/courseware/deletecourseware/",
                type: "delete",
                data: {
                    "courseware-id": delete_obj.val(),
                },
                success: function (data) {
                    if (data["status"] == "success") {
                        delete_obj.parent("div").parent("li").next("hr").remove();
                        delete_obj.parent("div").parent("li").remove();
                    } else if (data["status"] == "error") {
                        alert("删除失败")
                    }
                }
            })
        }
    })
});