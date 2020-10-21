$(function () {
    $("button[name='delete-question']").click(function () {
        var mymessage = confirm("确认删除问题？");
        if (mymessage == true) {
            var delete_obj = $(this);
            $.ajax({
                url: "/homework/deletequestion/",
                type: "post",
                data: {
                    "homework-id": $("input[name='homework-id']").val(),
                    "question-id": $(this).val(),
                    "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
                },
                success: function (data) {
                    if (data["status"] == "success") {
                        delete_obj.parent("li").remove();
                    } else if (data["status"] == "error") {
                        alert("删除失败")
                    }
                }
            })
        }
    });
    $(".delete-homework").click(function () {
        var mymessage = confirm("确认删除作业？");
        if (mymessage == true) {
            var delete_obj = $(this);
            $.ajax({
                url: "/homework/deletehomework/",
                type: "post",
                data: {
                    "homework-id": delete_obj.val(),
                    "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
                },
                success: function (data) {
                    if (data["status"] == "success") {
                        delete_obj.parent("span").parent("div").parent("li").remove();
                    } else if (data["status"] == "error") {
                        alert("删除失败")
                    }
                }
            })
        }
    })
});