$(function () {
    $(".pagination").find("li[class='page_number active']").each(function () {
        var a = $(this).find("a:first")[0];
        if ($(a).attr("href").split("/")[1] == location.pathname.split("/")[1]) {
            $(".nav li:nth-child(2)").addClass("active");
            $(".nav li:nth-child(2)").children("a").css("background-color", "#23b8ff");
        }
    });

    // click-nums
    $(".item-img-link").click(function () {
        $.ajax({
            url: "/video/clicknums/",
            type: "post",
            data: {
                "course-id": $(this).children("input[name='courseid']").val(),
                "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                console.log(data["status"])
            }
        })
    });
    $(".item-tt-link").click(function () {
        $.ajax({
            url: "/video/clicknums/",
            type: "post",
            data: {
                "course-id": $(this).children("input[name='courseid']").val(),
                "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                console.log(data["status"])
            }
        })
    });
    $(".item-carouel-img-link").click(function () {
        $.ajax({
            url: "/video/clicknums/",
            type: "post",
            data: {
                "course-id": $(this).children("input[name='courseid']").val(),
                "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                console.log(data["status"])
            }
        })
    });


   // video-player
    $(".js-study-task-list").find("li[class='sub-section']").each(function () {
        var a = $(this).find("a:first")[0];
        if ($(a).attr("href").split("/")[3] == location.pathname.split("/")[1]) {
            $(".nav li:nth-child(2)").addClass("active");
            $(".nav li:nth-child(2)").children("a").css("background-color", "#23b8ff");
        }
    });
    $(".js-study-task-list li a").each(function (v, elm) {
        var $a = $(this);
        if ($a.data('anchor').split("=").slice(2, 3)[0] == window.location.href.split("=").slice(2, 3)[0]) {
            $a.addClass("active");
            $a.css("color", "#23b8ff");
            $a.parent("li").children("div").children("span").css("color", "#23b8ff");
            $a.parent("li").children("div").children("button").css("color", "#23b8ff");
        }
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
    $(".delete-video").click(function () {
        var mymessage = confirm("确认删除视频？");
        var myVideo = document.getElementsByTagName('video')[0];   //获取视频video
        if (myVideo.play()) {
            myVideo.pause();
            myVideo.ended;
        } else if (myVideo.pause()) {
            myVideo.pause();
            myVideo.ended;
        } else {
            myVideo.pause();
            myVideo.ended;
        }
        if (mymessage == true) {
            var delete_obj = $(this);
            $.ajax({
                url: "/video/deletevideo/",
                type: "delete",
                data: {
                    "video-id": delete_obj.val(),
                    "course-id": $("input[name='course-id']").val(),
                },
                success: function (data) {
                    if (data["status"] == "success") {
                        delete_obj.parent("div").parent("li").remove();
                    } else if (data["status"] == "error") {
                        alert("删除失败")
                    } else if (data["status"] == "remove") {
                        window.location.href = "http://localhost:8000/video/"
                    }
                }
            })
        }
    });
    var options = {};
    var player = videojs('example_video_1', options, function onPlayerReady() {
        var time1;
        var t1 = 0;

        function aa() {
            t1 += 1;
            $("#aa").val(t1);
        }

        //开始播放视频时，设置一个定时器，每1秒调用一次aa(),观看时长加1秒
        this.on('play', function () {
            time1 = setInterval(function () {
                aa();
            }, 1000)
        });
        //结束和暂时时清除定时器，并向后台发送数据
        this.on('ended', function () {
            window.clearInterval(time1);
            var click_nums = 1;
            countTime(click_nums);   //向后台发数据
        });
        this.on('pause', function () {
            window.clearInterval(time1);
            var click_nums = 0;
            countTime(click_nums);  //向后台发数据
        });
        var closeBtn = player.controlBar.addChild("button").addClass("vjs-close");
        var vjs_close = $(".vjs-close");
        vjs_close.attr("title", "close");
        vjs_close.children("span:nth-child(1)").removeClass("vjs-icon-placeholder");
        vjs_close.children("span:nth-child(1)").addClass("glyphicon glyphicon-stop");
        vjs_close.click(function () {
            player.pause();
            player.hide();
            window.clearInterval(time1);
            var click_nums = 1;
            countTime(click_nums);   //向后台发数据
            $("video").attr("poster", "");
            $("video").attr("poster", "/media/" + $(".cover").val())
        })
    });
    //直接关闭页面，并向后台发送数据
    if (window.addEventListener) {
        var click_nums = 1;
        window.addEventListener("beforeunload", countTime(click_nums), false);
    } else {
        var click_nums = 1;
        window.attachEvent("onbeforeunload", countTime(click_nums));
    }

    function countTime(click_nums) {
        var sTime = $("#aa").val();
        var click_course = $("#click_course").val();
        if (click_nums == 1) {
            var click_number = click_nums;
        } else {
            var click_number = click_nums;
        }
        $.ajax({
            url: "/video/counttime/",
            type: "post",
            data: {
                "sTime": sTime,
                "click_number": click_number,
                "click_course": click_course,
                "vtitle": $("#bb").val(),
                "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val()
            }
        });
    }

    function formatSeconds(value) {
        var theTime = parseInt(value);// 秒
        var theTime1 = 0;// 分
        var theTime2 = 0;// 小时

        // alert(theTime);
        if (theTime > 60) {
            theTime1 = parseInt(theTime / 60);
            theTime = parseInt(theTime % 60);

            // alert(theTime1+"-"+theTime);
            if (theTime1 > 60) {
                theTime2 = parseInt(theTime1 / 60);
                theTime1 = parseInt(theTime1 % 60);
            }
        }
        var result = "" + parseInt(theTime) + "秒";
        if (theTime1 > 0) {
            result = "" + parseInt(theTime1) + "分" + result;
        }
        if (theTime2 > 0) {
            result = "" + parseInt(theTime2) + "小时" + result;
        }
        return result;
    }
});