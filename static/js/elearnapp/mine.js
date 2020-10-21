$(function () {
    $(".mine-item-title li").click(function () {
        if ($(this).children("a").html() == "上传视频") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-upload-video").removeAttr("hidden")
        } else if ($(this).children("a").html() == "上传课件") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-upload-courseware").removeAttr("hidden")
        } else if ($(this).children("a").html() == "添加作业") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-add-questions").removeAttr("hidden")
        } else if ($(this).children("a").html() == "我的作业") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-myhomework").removeAttr("hidden")
        } else if ($(this).children("a").html() == "批改作业") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-correct-homework").removeAttr("hidden")
        } else if ($(this).children("a").html() == "学习详情") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-student-details").removeAttr("hidden")
        } else if ($(this).children("a").html() == "学生分数") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-student-score").removeAttr("hidden")
        } else if ($(this).children("a").html() == "教授专业") {
            $(".mine-item-title li").removeAttr("style");
            $(this).css("background-color", "#23b8ff");
            $(".mine-item-content").children("div").attr("hidden", "hidden");
            $(".mine-item-add-specialty").removeAttr("hidden")
        }
    });

    $(".add-course").click(function () {
        $(".mine-item-upload-video").attr("hidden", "hidden");
        $(".mine-item-add-course").removeAttr("hidden");
    });

    $(".add-homework").click(function () {
        $(".mine-item-add-questions").attr("hidden", "hidden");
        $(".mine-item-add-homework").removeAttr("hidden");
    });
    $(".correct-homework").click(function () {
        var id = $(this).attr("name");
        $.ajax({
            url: "/homework/correct_student/",
            type: "get",
            data: {
                "homework-id": $(this).attr("name"),
            },
            success: function (data) {
                var data_obj = JSON.parse(data["data"]);
                for (i = 0; i < data_obj.length; i++) {
                    if ($(".mine-item-all-student-inner li").length < data_obj.length) {
                        $(".mine-item-all-student-inner").children("ul").append("<li><a href=" + "/homework/correct/?studentid=" + data_obj[i]['pk'] + "&homeworkid=" + id + " target='_blank'>" + data_obj[i]['fields']['name'] + "</a></li>")
                    }
                }
            }
        });
        $(".mine-item-correct-homework").attr("hidden", "hidden");
        $(".mine-item-all-student").removeAttr("hidden");
    });


    //上传课程
    $(".upload-course").click(function () {
        if ($("input[name='course-name']").val() == "") {
            $(".course-name-tip").css("display", "inline-block");
            return false;
        } else if ($("input[name='course-file']").val() == "") {
            $(".course-file-tip").css("display", "inline-block");
            return false;
        } else {
            var formData = new FormData($('#upload-course')[0]);
            $.ajax({
                type: "POST",
                url: "/video/uploadcourse/",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data["status"] == "success") {
                        $("input[name='course-name']").val("");
                        $("input[name='course-desc']").val("");
                        $("input[name='course-file']").val("");
                        $(".upload-course-error").css("display", "none");
                        $(".upload-course-success").css("display", "block");

                        setTimeout(function () {
                            $(".upload-course-success").css("display", "none");
                            window.location.href = "http://localhost:8000/mine";
                        }, 1000);
                    } else if (data["status"] == "error") {
                        $(".upload-course-success").css("display", "none");
                        $(".upload-course-error").css("display", "block");
                        setTimeout(function () {
                            $(".upload-course-error").css("display", "none");
                        }, 5000);
                    }
                }
            });
        }
    });

    //上传视频
    $(".upload-video").click(function () {
        if ($("select[name='course-select'] option:selected").val() == undefined) {
            $(".option-tip2").css("display", "none");
            $(".option-tip").css("display", "inline-block");
        } else if ($("input[name='video-name']").val() == "") {
            $(".video-name-tip").css("display", "inline-block");
        } else if ($("input[name='video-file']").val() == "") {
            $(".video-file-tip").css("display", "inline-block");
        } else {
            var formData = new FormData($('#upload-video')[0]);
            $.ajax({
                type: "POST",
                url: "/video/uploadvideo/",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data["status"] == "success") {
                        $("input[name='video-title']").val("");
                        $("input[name='video-file']").val("");
                        $(".upload-video-error").css("display", "none");
                        $(".upload-video-success").css("display", "block");
                        setTimeout(function () {
                            $(".upload-video-success").css("display", "none");
                        }, 5000);
                    } else if (data["status"] == "error") {
                        $(".upload-video-success").css("display", "none");
                        $(".upload-video-error").css("display", "block");
                        setTimeout(function () {
                            $(".upload-video-error").css("display", "none");
                        }, 5000);
                    }
                }
            });
        }
    });

    //上传课件
    $(".upload").click(function () {
        if ($("select[name='courseware-specialty-select'] option:selected") == "") {
            $(".courseware-specialty-select-tip").css("display", "inline-block")
        } else if ($("input[name='courseware-name']").val() == "") {
            $(".courseware-name-tip").css("display", "inline-block")
        } else if ($("input[name='courseware-file']").val() == "") {
            $(".courseware-file-tip").css("display", "inline-block")
        } else {
            var formData = new FormData($('#upload-courseware')[0]);
            $.ajax({
                type: "POST",
                url: "/courseware/upload/",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data["status"] == "success") {
                        $("input[name='courseware-name']").val("");
                        $("input[name='courseware-file']").val("");
                        $(".upload-error").css("display", "none");
                        $(".upload-success").css("display", "block");
                        setTimeout(function () {
                            $(".upload-success").css("display", "none");
                        }, 5000);
                    } else if (data["status"] == "error") {
                        $(".upload-success").css("display", "none");
                        $(".upload-error").css("display", "block");
                        setTimeout(function () {
                            $(".upload-error").css("display", "none");
                        }, 5000);
                    }
                }
            });
        }
    });

    //增加作业
    $(".upload-homework").click(function () {
        if ($("select[name='homework-specialty-select'] option:selected") == "") {
            $(".homework-specialty-select-tip").css("display", "inline-block")
        } else if ($("input[name='homework-name']").val() == "") {
            $(".homework-name-tip").css("display", "inline-block")
        } else {
            var formData = new FormData($('#upload-homework')[0]);
            $.ajax({
                type: "POST",
                url: "/homework/upload/",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data["status"] == "success") {
                        $("input[name='homework-name']").val("");
                        $("input[name='homework-desc']").val("");
                        $(".upload-homework-error").css("display", "none");
                        $(".upload-homework-success").css("display", "block");
                        setTimeout(function () {
                            $(".upload-homework-success").css("display", "none");
                            window.location.href = "http://localhost:8000/mine";
                        }, 1000);
                    } else if (data["status"] == "error") {
                        $(".upload-homework-success").css("display", "none");
                        $(".upload-homework-error").css("display", "block");
                        setTimeout(function () {
                            $(".upload-homework-error").css("display", "none");
                        }, 5000);
                    }
                }
            });
        }
    });

    //增加判断题
    $(".add-pd-question").click(function () {
        if ($("select[name='homework-select'] option:selected").val() == undefined) {
            $(".homework-select-tip").css("display", "block")
        } else if ($("textarea[name='pd-question']").val() == "") {
            $(".pd-question-tip").css("display", "block")
        } else if ($("input[name='pd-answer']:checked").val() == undefined) {
            $(".pd-answer-tip").css("display", "block")
        } else {
            $.ajax({
                url: "/homework/addpd/",
                type: "post",
                data: {
                    "homework": $("select[name='homework-select'] option:selected").val(),
                    "pd-question": $("textarea[name='pd-question']").val(),
                    "pd-answer": $("input[name='pd-answer']:checked").val(),
                    "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
                },
                success: function (data) {
                    if (data["status"] == "success") {
                        $("textarea[name='pd-question']").val("");
                        $("input[name='pd-answer']").removeAttr("checked");
                        $(".add-question-error").css("display", "none");
                        $(".add-question-success").css("display", "block");
                        setTimeout(function () {
                            $(".add-question-success").css("display", "none");
                        }, 5000);
                    } else if (data["status"] == "error") {
                        $(".add-question-success").css("display", "none");
                        $(".add-question-error").css("display", "block");
                        setTimeout(function () {
                            $(".add-question-error").css("display", "none");
                        }, 5000);
                    }
                }
            })
        }
    });
    $("select[name='homework-select']").change(function () {
        $(".homework-select-tip").css("display", "none")
    });
    $("textarea[name='pd-question']").change(function () {
        $(".pd-question-tip").css("display", "none")
    });
    $("input[name='pd-answer']").change(function () {
        $(".pd-answer-tip").css("display", "none")
    });

    //增加选择题
    $(".add-xz-question").click(function () {
        var xz_question = $("textarea[name='xz-question']").val();
        var xz_answer_A = $("input[name='xz-answer-A']").val();
        var xz_answer_B = $("input[name='xz-answer-B']").val();
        var xz_answer_C = $("input[name='xz-answer-C']").val();
        var xz_answer_D = $("input[name='xz-answer-D']").val();
        if ($("select[name='homework-select'] option:selected").val() == undefined) {
            $(".homework-select-tip").css("display", "block")
        } else if (xz_question == "") {
            $(".xz-question-tip").css("display", "block")
        } else if (xz_answer_A == "") {
            $(".xz-answer-A-tip").css("display", "block")
        } else if (xz_answer_B == "") {
            $(".xz-answer-B-tip").css("display", "block")
        } else if (xz_answer_C == "") {
            $(".xz-answer-C-tip").css("display", "block")
        } else if (xz_answer_D == "") {
            $(".xz-answer-D-tip").css("display", "block")
        } else if ($("input[name='xz-answer']:checked").val() == undefined) {
            $(".xz-answer-tip").css("display", "block")
        } else {
            $.ajax({
                url: "/homework/addxz/",
                type: "post",
                data: {
                    "homework": $("select[name='homework-select'] option:selected").val(),
                    "xz-question": xz_question,
                    "xz-answer-A": xz_answer_A,
                    "xz-answer-B": xz_answer_B,
                    "xz-answer-C": xz_answer_C,
                    "xz-answer-D": xz_answer_D,
                    "xz-answer": $("input[name='xz-answer']:checked").val(),
                    "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
                },
                success: function (data) {
                    if (data["status"] == "success") {
                        $("textarea[name='xz-question']").val("");
                        $("input[name='xz-answer-A']").val("");
                        $("input[name='xz-answer-B']").val("");
                        $("input[name='xz-answer-C']").val("");
                        $("input[name='xz-answer-D']").val("");
                        $("input[name='xz-answer']").removeAttr("checked");
                        $(".add-question-error").css("display", "none");
                        $(".add-question-success").css("display", "block");
                        setTimeout(function () {
                            $(".add-question-success").css("display", "none");
                        }, 5000);
                    } else if (data["status"] == "error") {
                        $(".add-question-success").css("display", "none");
                        $(".add-question-error").css("display", "block");
                        setTimeout(function () {
                            $(".add-question-error").css("display", "none");
                        }, 5000);
                    }
                }
            })
        }
    });
    $("textarea[name='xz-question']").change(function () {
        $(".xz-question-tip").css("display", "none")
    });
    $("input[name='xz-answer-A']").change(function () {
        $(".xz-answer-A-tip").css("display", "none")
    });
    $("input[name='xz-answer-B']").change(function () {
        $(".xz-answer-B-tip").css("display", "none")
    });
    $("input[name='xz-answer-C']").change(function () {
        $(".xz-answer-C-tip").css("display", "none")
    });
    $("input[name='xz-answer-D']").change(function () {
        $(".xz-answer-D-tip").css("display", "none")
    });
    $("input[name='xz-answer']").change(function () {
        $(".xz-answer-tip").css("display", "none")
    });


    //简答题
    $(".add-jd-question").click(function () {
        if ($("select[name='homework-select'] option:selected").val() == undefined) {
            $(".homework-select-tip").css("display", "block")
        } else if ($("textarea[name='jd-question']").val() == "") {
            $(".jd-question-tip").css("display", "block")
        } else {
            $.ajax({
                url: "/homework/addjd/",
                type: "post",
                data: {
                    "homework": $("select[name='homework-select'] option:selected").val(),
                    "jd-question": $("textarea[name='jd-question']").val(),
                    "jd-answer": $("textarea[name='jd-answer']").val(),
                    "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
                },
                success: function (data) {
                    if (data["status"] == "success") {
                        $("textarea[name='jd-question']").val("");
                        $("textarea[name='jd-answer']").val("");
                        $(".add-question-error").css("display", "none");
                        $(".add-question-success").css("display", "block");
                        setTimeout(function () {
                            $(".add-question-success").css("display", "none");
                        }, 5000);
                    } else if (data["status"] == "error") {
                        $(".add-question-success").css("display", "none");
                        $(".add-question-error").css("display", "block");
                        setTimeout(function () {
                            $(".add-question-error").css("display", "none");
                        }, 5000);
                    }
                }
            })
        }
    });
    $("textarea[name='jd-question']").change(function () {
        $(".jd-question-tip").css("display", "none")
    });

    $("select[name='course-select']").change(function () {
        $(".option-tip").css("display", "none");
        $(".option-tip2").css("display", "inline-block");
    });
    $("input[name='video-name']").change(function () {
        $(".video-name-tip").css("display", "none");
    });
    $("input[name='video-file']").change(function () {
        $(".video-file-tip").css("display", "none");
    });
    $("input[name='course-name']").change(function () {
        $(".course-name-tip").css("display", "none");
    });
    $("input[name='course-file']").change(function () {
        $(".course-file-tip").css("display", "none");
    });
    $("input[name='courseware-name']").change(function () {
        $(".courseware-name-tip").css("display", "none")
    });
    $("input[name='courseware-file']").change(function () {
        $(".courseware-file-tip").css("display", "none")
    });
    $("input[name='homework-name']").change(function () {
        $(".homework-name-tip").css("display", "none")
    });


    //增加的题目类型标题颜色和显示内容
    $(".pd").click(function () {
        $(this).css("color", "#12a7ff");
        $(".xz").css("color", "#333333");
        $(".jd").css("color", "#333333");
        $(".mine-item-xz").attr("hidden", "hidden");
        $(".mine-item-jd").attr("hidden", "hidden");
        $(".mine-item-pd").removeAttr("hidden")
    });
    $(".xz").click(function () {
        $(this).css("color", "#12a7ff");
        $(".pd").css("color", "#333333");
        $(".jd").css("color", "#333333");
        $(".mine-item-pd").attr("hidden", "hidden");
        $(".mine-item-jd").attr("hidden", "hidden");
        $(".mine-item-xz").removeAttr("hidden")
    });
    $(".jd").click(function () {
        $(this).css("color", "#12a7ff");
        $(".pd").css("color", "#333333");
        $(".xz").css("color", "#333333");
        $(".mine-item-pd").attr("hidden", "hidden");
        $(".mine-item-xz").attr("hidden", "hidden");
        $(".mine-item-jd").removeAttr("hidden")
    });


    $(".release-homework").click(function () {
        $.ajax({
            url: "/homework/release/",
            type: "post",
            data: {
                "homeworkid": $(this).val(),
                "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val()
            },
            success: function (data) {
                if (data["status"] == "success") {
                    alert("发布成功");
                    window.location.href = "http://localhost:8000/mine/"
                } else {
                    alert("发布失败，请重新发布")
                }
            }
        })
    });
});

