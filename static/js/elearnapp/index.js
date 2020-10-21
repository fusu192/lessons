$(function () {
    $(".nav").find("li").each(function () {
        var a = $(this).find("a:first")[0];
        if ($(a).attr("href") == location.pathname) {
            $(this).addClass("active");
            $(this).children("a").css("background-color", "#23b8ff")
        } else {
            $(this).removeClass("active");
            $(this).children("a").css("background-color", "#ffffff")
        }

        if ($(a).attr("href") == "/" + location.pathname.split("/")[1] + "/") {
            $(this).addClass("active");
            $(this).children("a").css("background-color", "#23b8ff")
        } else {
            $(this).removeClass("active");
            $(this).children("a").css("background-color", "#ffffff")
        }
    });

    $('#register').click(function () {
        $('#registerModal').modal('show') //注册弹出框
    });
    $('#goregister').click(function () {
        $('#registerModal').modal('show') //注册弹出框
    });

    $('#login').click(function () {
        $('#loginModal').modal('show') //登录弹出框
    });
    $('#gologin').click(function () {
        $('#loginModal').modal('show') //登录弹出框
    });

    $('#resetpassword').click(function () {
        $('#resetPasswordModal').modal('show') //修改密码弹出框
    });

    $('.dropdown-toggle').mouseover(function () {
        $(this).attr("aria-expanded", true);
        $(".personal-center").addClass("open")
    });
    $(".dropdown-menu li").mouseover(function () {
        $(this).children('a').css("color", "#12a7ff");
    });
    $(".dropdown-menu li").mouseout(function () {
        $(this).children('a').css("color", "#333333");
    });

    $('#resethead').click(function () {
        $('#resetheadModal').modal('show') //修改头像弹出框
    });

    $(".r-st").change(function () {
        if ($(this).val() == "teacher") {
            $(".v-code").removeAttr("hidden"); //如果选择教师注册，显示注册码输入框
            $(".r-st[value='student']").removeAttr("checked");
            $(".r-st[value='teacher']").attr('checked', 'checked');
            $(".specialty-select-outter-div").attr("hidden", "hidden")
        } else {
            $(".v-code").attr("hidden", "hidden"); //如果选择教师注册，隐藏注册码输入框
            $(".r-st[value='student']").attr('checked', 'checked');
            $(".r-st[value='teacher']").removeAttr("checked");
            $(".specialty-select-outter-div").removeAttr("hidden")
        }
    });


    //注册验证
    $(".register-submit").click(function () {
            var college = $("#college-select option:selected");
            var specialty = $("#specialty-select option:selected");
            var name = $("input[name='register-name']");
            var number = $("input[name='register-number']");
            var password = $("input[name='register-password']");
            var password2 = $("input[name='register-password-2']");
            var identity = $(".r-st:checked");
            var code = $("input[name='code-tip']");
            var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']");

            var college_select_tip = $(".college-select-tip");
            var specialty_select_tip = $(".specialty-select-tip");
            var r_name_tip = $(".r-name-tip");
            var r_number_tip = $(".r-number-tip");
            var r_password_tip = $(".r-password-tip");
            var r_password2_tip = $(".r-password-tip-2");
            var tips = $(".tips");
            var code_tip = $(".code-tip");

            //如果注册信息没有一个为空执行if
            if (college.val() != "" && name.val() != "" && number.val() != "" && password.val() != "" && password2.val() != "") {
                college_select_tip.css("display", "none");
                specialty_select_tip.css("display", "none");
                r_name_tip.html("");
                r_number_tip.html(""); //清空三个提示
                r_password_tip.html("");
                r_password2_tip.html("");

                //如果选择学生注册
                if (identity.val() == "student") {
                    if (specialty.val() == "") {
                        specialty_select_tip.css("display", "block")
                    } else if (number.val().length < 8) {
                        r_number_tip.css("display", "block").html("不能小于8位");
                        name.change(function () {
                            r_number_tip.html("")
                        });
                    } else if (number.val().length > 15) {
                        r_number_tip.css("display", "block").html("不能大于15位");
                        name.change(function () {
                            r_number_tip.html("")
                        });
                    } else if (/^[0-9]+$/.test(number.val())) {
                        if (password.val().length < 6) {
                            r_password_tip.css("display", "block").html("不能小于6位");
                            password.change(function () {
                                r_password_tip.html("")
                            });
                        } else if (password.val().length > 15) {
                            r_password_tip.css("display", "block").html("不能大于15位");
                            password.change(function () {
                                r_password_tip.html("")
                            });
                        } else if (password.val() != password2.val()) {
                            r_password2_tip.css("display", "block").html("两次输入的密码不一致");
                            password.change(function () {
                                r_password2_tip.html("")
                            });
                            password2.change(function () {
                                r_password2_tip.html("")
                            });
                        } else {
                            $.ajax({
                                url: "/mine/studentregister/",
                                type: "post",
                                data: {
                                    "college": college.val(),
                                    "specialty": specialty.val(),
                                    "name": name.val(),
                                    "number": number.val(),
                                    "password": password.val(),
                                    "identity": identity.val(),
                                    "csrfmiddlewaretoken": csrfmiddlewaretoken.val(),
                                },
                                success: function (data) {
                                    var tips = $(".tips");
                                    if (data["status"] == "ok") {
                                        tips.html("<div>注册成功！</div><br><div><span id='mes'>3</span>秒后自动跳转...</div>");
                                        tips.css({"text-align": "center", "font-size": "20px"});

                                        var tt = 3;

                                        function a() {
                                            if (tt == 1) {
                                                window.location.reload() //注册成功后定时刷新网页
                                            } else {
                                                tt--;
                                                $("#mes").html(tt);
                                            }
                                        }

                                        setInterval(a, 1000);

                                    } else if (data["status"] == "error") {
                                        r_number_tip.css("display", "block").html("学号已存在<a id='reset' href='javascript:void(0)' style='display: block;text-decoration: none;text-align: right;margin-top: -20px;'>不是本人？请联系管理员</a>");
                                        number.change(function () {
                                            r_number_tip.html("")
                                        });
                                    } else if (data["status"] == "stop") {
                                        r_name_tip.css("display", "block").html("服务器出错，请重新提交");
                                        name.change(function () {
                                            r_name_tip.html("")
                                        });
                                    }
                                }
                            });
                        }
                    } else {
                        specialty_select_tip.css("display", "none");
                        r_number_tip.css("display", "block").html("必须全为数字");
                        number.change(function () {
                            r_number_tip.html("")
                        });
                    }

                }
                //如果选择教师注册
                else if (identity.val() == "teacher") {
                    if (number.val().length < 8) {
                        r_number_tip.css("display", "block").html("不能小于8位");
                        number.change(function () {
                            r_number_tip.html("")
                        });
                    } else if (number.val().length > 15) {
                        r_number_tip.css("display", "block").html("不能大于15位");
                        number.change(function () {
                            r_number_tip.html("")
                        });
                    } else if (/^[0-9]+$/.test(number.val())) {
                        if (password.val().length < 6) {
                            r_password_tip.css("display", "block").html("不能小于6位");
                            password.change(function () {
                                r_password_tip.html("")
                            });
                        } else if (password.val().length > 15) {
                            r_password_tip.css("display", "block").html("不能大于15位");
                            password.change(function () {
                                r_password_tip.html("")
                            });
                        } else {
                            if (code.val() != "") {
                                if (password.val() != password2.val()) {
                                    r_password2_tip.css("display", "block").html("两次输入的密码不一致");
                                    password.change(function () {
                                        r_password2_tip.html("")
                                    });
                                    password2.change(function () {
                                        r_password2_tip.html("")
                                    });
                                } else {
                                    $.ajax({
                                        url: "/mine/teacherregister/",
                                        type: "post",
                                        data: {
                                            "college": college.val(),
                                            "name": name.val(),
                                            "number": number.val(),
                                            "password": password.val(),
                                            "identity": identity.val(),
                                            "code": code.val(),
                                            "csrfmiddlewaretoken": csrfmiddlewaretoken.val(),
                                        },
                                        success: function (data) {
                                            if (data["code"] == "ok") {
                                                if (data["status"] == "ok") {
                                                    tips.html("<div>注册成功！</div><br><div><span id='mes'>3</span>秒后自动跳转...</div>");
                                                    tips.css({"text-align": "center", "font-size": "20px"});

                                                    var tt = 3;

                                                    function a() {
                                                        if (tt == 1) {
                                                            window.location.reload() //注册成功后定时刷新网页
                                                        } else {
                                                            tt--;
                                                            $("#mes").html(tt);
                                                        }
                                                    }

                                                    setInterval(a, 1000);

                                                } else if (data["status"] == "error") {
                                                    r_number_tip.css("display", "block").html("学号已存在<a id='reset' href='javascript:void(0)' style='display: block;text-decoration: none;text-align: right;margin-top: -20px;'>不是本人？请联系管理员</a>");

                                                    number.change(function () {
                                                        r_number_tip.html("")
                                                    });
                                                } else if (data["status"] == "stop") {
                                                    r_name_tip.css("display", "block").html("服务器出错，请重新提交");
                                                    name.change(function () {
                                                        r_name_tip.html("")
                                                    });
                                                }
                                            } else if (data["code"] == "error") {
                                                code_tip.css("display", "block").html("注册码不正确");
                                                code.change(function () {
                                                    code_tip.html("")
                                                })
                                            }
                                        }
                                    });
                                }

                            } else {
                                code_tip.css("display", "block").html("注册码不能为空");
                                code.change(function () {
                                    code_tip.html("")
                                })
                            }

                        }
                    } else {
                        r_number_tip.css("display", "block").html("必须全为数字");
                        number.change(function () {
                            r_number_tip.html("")
                        });
                    }
                } else {
                    r_password2_tip.css("display", "block").html("请选择你的身份"); //两个身份都未选择时提示
                    $(".r-st").change(function () {
                        r_password2_tip.html("");
                    })
                }
            }
            //如果注册信息有一个为空执行else
            else {
                //判断哪一个为空
                if (college.val() == "") {
                    college_select_tip.css("display", "block")
                }
                if (name.val() == "") {
                    r_name_tip.css("display", "block").html("姓名不能为空")
                }
                if (number.val() == "") {
                    r_number_tip.css("display", "block").html("学号不能为空")
                }
                if (password.val() == "") {
                    r_password_tip.css("display", "block").html("密码不能为空")
                }
                if (password2.val() == "") {
                    r_password2_tip.css("display", "block").html("此处不能为空")
                }

                $("#college-select").change(function () {
                    if ($(this).val() == "") {
                        college_select_tip.css("display", "block")
                    } else {
                        college_select_tip.css("display", "none")
                    }
                });
                name.change(function () {
                    if ($(this).val() == "") {
                        r_name_tip.css("display", "block").html("姓名不能为空")
                    } else {
                        r_name_tip.html("")
                    }
                });
                number.change(function () {
                    if ($(this).val() == "") {
                        r_number_tip.css("display", "block").html("学号不能为空")
                    } else {
                        r_number_tip.html("")
                    }
                });
                password.change(function () {
                    if ($(this).val() == "") {
                        r_password_tip.css("display", "block").html("密码不能为空")
                    } else {
                        r_password_tip.html("")
                    }
                });
                password2.change(function () {
                    if ($(this).val() == "") {
                        r_password2_tip.css("display", "block").html("此处不能为空")
                    } else {
                        r_password2_tip.html("")
                    }
                })
            }
            if (specialty.val() == "") {
                specialty_select_tip.css("display", "block")
            }
            $("#specialty-select").change(function () {
                if ($(this).val() == "") {
                    specialty_select_tip.css("display", "block")
                } else {
                    specialty_select_tip.css("display", "none")
                }
            });
        }
    );


    $(".l-st").change(function () {
        if ($(this).val() == "teacher") {
            $(".l-st[value='student']").removeAttr("checked");
            $(".l-st[value='teacher']").attr('checked', 'checked')
        } else {
            $(".l-st[value='student']").attr('checked', 'checked');
            $(".l-st[value='teacher']").removeAttr("checked")
        }
    });


    //登录验证
    $(".login-submit").click(function () {
        var number = $("input[name='login-number']");
        var password = $("input[name='login-password']");
        var identity = $(".l-st:checked");
        var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']");

        var l_number_tip = $(".l-number-tip");
        var l_password_tip = $(".l-password-tip");
        var tips2 = $(".tips2");
        //如果登录信息没有一个为空执行if
        if (number.val() != "" && password.val() != "") {
            l_number_tip.html("");
            l_password_tip.html("");
            //如果选择学生登录
            if (identity.val() == "student") {
                $.ajax({
                    url: "/mine/studentlogin/",
                    type: "post",
                    data: {
                        "number": number.val(),
                        "password": password.val(),
                        "identity": identity.val(),
                        "csrfmiddlewaretoken": csrfmiddlewaretoken.val(),
                    },
                    success: function (data) {
                        if (data["status"] == "log_ok") {
                            tips2.html("<div>登录成功！</div><br><div><span id='l_mes'>1</span>秒后自动跳转...</div>");
                            tips2.css({"text-align": "center", "font-size": "20px"});

                            var tt = 1;

                            function b() {
                                if (tt == 1) {
                                    window.location.reload() //注册成功后定时刷新网页
                                } else {
                                    tt--;
                                    $("#l_mes").html(tt);
                                }
                            }

                            setInterval(b, 1000);
                        } else if (data["status"] == "log_error") {
                            l_password_tip.css("display", "block").html("密码错误<a hidden data-toggle='modal' id='forget' href='javascript:void(0)' style='display: block;text-decoration: none;text-align: right;margin-top: -20px;'>忘记密码请联系管理员</a>");

                            password.change(function () {
                                l_password_tip.html("")
                            })
                        } else if (data["status"] == "log_stop") {
                            l_password_tip.css("display", "block").html("服务器出错，请重新登录");
                            password.change(function () {
                                l_password_tip.html("")
                            })
                        } else if (data["status"] == "log_empty") {
                            l_number_tip.css("display", "block").html("学号不存在，请先注册");
                            number.change(function () {
                                l_number_tip.html("")
                            })
                        }
                    }
                })

            }
            //如果选择教师登录
            else if (identity.val() == "teacher") {
                $.ajax({
                    url: "/mine/teacherlogin/",
                    type: "post",
                    data: {
                        "number": number.val(),
                        "password": password.val(),
                        "identity": identity.val(),
                        "csrfmiddlewaretoken": csrfmiddlewaretoken.val(),
                    },
                    success: function (data) {
                        if (data["status"] == "log_ok") {
                            tips2.html("<div>登录成功！</div><br><div><span id='l_mes'>1</span>秒后自动跳转...</div>");
                            tips2.css({"text-align": "center", "font-size": "20px"});

                            var tt = 1;

                            function b() {
                                if (tt == 1) {
                                    window.location.reload() //注册成功后定时刷新网页
                                } else {
                                    tt--;
                                    $("#l_mes").html(tt);
                                }
                            }

                            setInterval(b, 1000);
                        } else if (data["status"] == "log_error") {
                            l_password_tip.css("display", "block").html("密码错误<a data-toggle='modal' id='forget' href='javascript:void(0)' style='display: block;text-decoration: none;text-align: right;margin-top: -20px;'>忘记密码请联系管理员</a>");

                            password.change(function () {
                                l_password_tip.html("")
                            })
                        } else if (data["status"] == "log_stop") {
                            l_password_tip.css("display", "block").html("服务器出错，请重新登录");
                            password.change(function () {
                                l_password_tip.html("")
                            })
                        } else if (data["status"] == "log_empty") {
                            l_number_tip.css("display", "block").html("学号不存在，请先注册");
                            number.change(function () {
                                l_number_tip.html("")
                            })
                        }
                    }
                });
            } else {
                l_password_tip.css("display", "block").html("请选择你的身份"); //两个身份都未选择时提示
                $(".tt").change(function () {
                    l_password_tip.html("");
                })
            }
        }
        //如果登录信息有一个为空执行else
        else {
            //判断哪一个为空
            if (number.val() == "") {
                l_number_tip.css("display", "block").html("学号不能为空")
            }
            if (password.val() == "") {
                l_password_tip.css("display", "block").html("密码不能为空")
            }

            number.change(function () {
                if ($(this).val() == "") {
                    l_number_tip.css("display", "block").html("学号不能为空")
                } else {
                    l_number_tip.html("")
                }
            });
            password.change(function () {
                if ($(this).val() == "") {
                    l_password_tip.css("display", "block").html("密码不能为空")
                } else {
                    l_password_tip.html("")
                }
            })
        }
    });

    // 修改密码
    $(".reset-password-submit").click(function () {
        var password_1 = $("input[name='reset-password-1']");
        var password_2 = $("input[name='reset-password-2']");
        
        var reset_password_tip_1 = $(".reset-password-tip-1");
        var reset_password_tip_2 = $(".reset-password-tip-2");
        var tips3 = $(".tips3");
        if (password_1.val() !== "" && password_2.val() !== "") {
            if (password_1.val().length < 6) {
                reset_password_tip_1.css("display", "block").html("不能小于6位");
                password_1.change(function () {
                    reset_password_tip_1.html("")
                });
            } else if (password_1.val().length > 15) {
                reset_password_tip_1.css("display", "block").html("不能大于15位");
                password_1.change(function () {
                    reset_password_tip_1.html("")
                });
            } else if (password_1.val() !== password_2.val()) {
                reset_password_tip_2.css("display", "block").html("两次输入的密码不一致");
                password_1.change(function () {
                    reset_password_tip_2.html("")
                });
                password_2.change(function () {
                    reset_password_tip_2.html("")
                });
            } else {
                $.ajax({
                    url: "/mine/resetpassword/",
                    type: "post",
                    data: {
                        "password": password_1.val(),
                        "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val()
                    },
                    success: function (data) {
                        if (data["status"] == "success") {
                            tips3.html("<div>密码修改成功！</div><br><div><span id='mes'>3</span>秒后自动跳转...</div>");
                            tips3.css({"text-align": "center", "font-size": "20px"});

                            var tt = 3;

                            function a() {
                                if (tt == 1) {
                                    window.location.reload() //修改成功后定时刷新网页
                                } else {
                                    tt--;
                                    $("#mes").html(tt);
                                }
                            }

                            setInterval(a, 1000);
                        } else if (data["status"] == "error") {
                            reset_password_tip_2.css("display", "block").html("不能修改<a id='reset' href='javascript:void(0)' style='display: block;text-decoration: none;text-align: right;margin-top: -20px;'>请联系管理员</a>");

                            password_1.change(function () {
                                reset_password_tip_1.html("")
                            });
                            password_2.change(function () {
                                reset_password_tip_2.html("")
                            });
                        } else if (data["status"] == "stop") {
                            reset_password_tip_2.css("display", "block").html("服务器出错，请重新提交");
                            password_1.change(function () {
                                reset_password_tip_1.html("")
                            });
                            password_2.change(function () {
                                reset_password_tip_2.html("")
                            });
                        } else if (data["status"] == "same") {
                            reset_password_tip_2.css("display", "block").html("新密码不能与原密码相同");
                            password_1.change(function () {
                                reset_password_tip_2.html("")
                            });
                            password_2.change(function () {
                                reset_password_tip_2.html("")
                            });
                        }
                    }
                });
            }
        } else {
            if (password_1.val() == "") {
                reset_password_tip_1.css("display", "block").html("密码不能为空")
            }
            if (password_2.val() == "") {
                reset_password_tip_2.css("display", "block").html("密码不能为空")
            }
            password_1.change(function () {
                if ($(this).val() == "") {
                    reset_password_tip_1.css("display", "block").html("密码不能为空")
                } else {
                    reset_password_tip_1.html("")
                }
            });
            password_2.change(function () {
                if ($(this).val() == "") {
                    reset_password_tip_2.css("display", "block").html("密码不能为空")
                } else {
                    reset_password_tip_2.html("")
                }
            });
        }
    });

    $(".login-password-eye").click(function () {
        var login_password_eye_icon = $(".login-password-eye-icon");
        if (login_password_eye_icon.hasClass("glyphicon-eye-close")) {
            login_password_eye_icon.removeClass("glyphicon-eye-close");
            login_password_eye_icon.addClass("glyphicon-eye-open");
            $("input[name='login-password']").attr("type", "text")
        } else if (login_password_eye_icon.hasClass("glyphicon-eye-open")) {
            login_password_eye_icon.removeClass("glyphicon-eye-open");
            login_password_eye_icon.addClass("glyphicon-eye-close");
            $("input[name='login-password']").attr("type", "password")
        }
    });
    $(".register-password-eye-1").click(function () {
        var password = $("input[name='register-password']");
        var register_password_eye_icon_1 = $(".register-password-eye-icon-1");
        if (register_password_eye_icon_1.hasClass("glyphicon-eye-close")) {
            register_password_eye_icon_1.removeClass("glyphicon-eye-close");
            register_password_eye_icon_1.addClass("glyphicon-eye-open");
            password.attr("type", "text")
        } else if (register_password_eye_icon_1.hasClass("glyphicon-eye-open")) {
            register_password_eye_icon_1.removeClass("glyphicon-eye-open");
            register_password_eye_icon_1.addClass("glyphicon-eye-close");
            password.attr("type", "password")
        }
    });
    $(".register-password-eye-2").click(function () {
        var password2 = $("input[name='register-password-2']");
        var register_password_eye_icon_2 = $(".register-password-eye-icon-2");
        if (register_password_eye_icon_2.hasClass("glyphicon-eye-close")) {
            register_password_eye_icon_2.removeClass("glyphicon-eye-close");
            register_password_eye_icon_2.addClass("glyphicon-eye-open");
            password2.attr("type", "text")
        } else if (register_password_eye_icon_2.hasClass("glyphicon-eye-open")) {
            register_password_eye_icon_2.removeClass("glyphicon-eye-open");
            register_password_eye_icon_2.addClass("glyphicon-eye-close");
            password2.attr("type", "password")
        }
    });
    $(".reset-password-eye-1").click(function () {
        var reset_password_eye_icon_1 = $(".reset-password-eye-icon-1");
        if (reset_password_eye_icon_1.hasClass("glyphicon-eye-close")) {
            reset_password_eye_icon_1.removeClass("glyphicon-eye-close");
            reset_password_eye_icon_1.addClass("glyphicon-eye-open");
            $("input[name='reset-password-1']").attr("type", "text")
        } else if (reset_password_eye_icon_1.hasClass("glyphicon-eye-open")) {
            reset_password_eye_icon_1.removeClass("glyphicon-eye-open");
            reset_password_eye_icon_1.addClass("glyphicon-eye-close");
            $("input[name='reset-password-1']").attr("type", "password")
        }
    });

    $(".reset-password-eye-2").click(function () {
        var reset_password_eye_icon_2 = $(".reset-password-eye-icon-2");
        if (reset_password_eye_icon_2.hasClass("glyphicon-eye-close")) {
            reset_password_eye_icon_2.removeClass("glyphicon-eye-close");
            reset_password_eye_icon_2.addClass("glyphicon-eye-open");
            $("input[name='reset-password-2']").attr("type", "text")
        } else if (reset_password_eye_icon_2.hasClass("glyphicon-eye-open")) {
            reset_password_eye_icon_2.removeClass("glyphicon-eye-open");
            reset_password_eye_icon_2.addClass("glyphicon-eye-close");
            $("input[name='reset-password-2']").attr("type", "password")
        }
    });
    $(".head-picture-submit").click(function () {
        var head_picture = $("input[name='head-picture']").val();
        var formData = new FormData($('#head-picture-form')[0]);
        if (head_picture !== "") {
            $.ajax({
                url: "/mine/headpicture/",
                type: "post",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                // data: {
                //     "head_picture": head_picture,
                //     "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
                // },
                success: function (data) {
                    if (data["status"] == "success") {
                        $(".profile-photo").attr("src", "/static/" + data["photo"]);
                        $('#resetheadModal').modal('hide') //修改头像弹出框
                    } else if (data["status"] == "error") {
                        $(".head-picture-error-tip").css("display", "block")
                    } else if (data["status"] == "stop") {
                        $(".head-picture-error-tip").css("display", "block")
                    }
                }
            })
        } else {
            $(".head-picture-tip").css("display", "block")
        }
    });
    $("input[name='head-picture']").change(function () {
        if ($("input[name='head-picture']").val() !== "") {
            $(".head-picture-tip").css("display", "none");
        }
        $(".head-picture-error-tip").css("display", "none")
    });


    // $.ajax({
    //     url: "/mine/specialty/",
    //     type: "get",
    //     data: {
    //         "college": Number($("#college-select option:selected").val())
    //     },
    //     success: function (data) {
    //         for (var i = -1; i < data["data"].length; i++) {
    //             if (i == -1) {
    //                 $("#specialty-select").append("<option value=''></option>");
    //             } else {
    //                 $("#specialty-select").append("<option value=" + data['data'][i]['id'] + ">" + data['data'][i]['name'] + "</option>");
    //             }
    //
    //         }
    //     }
    // });
    $("#college-select").change(function () {
        $("#specialty-select").empty();
        $.ajax({
            url: "/mine/specialty/",
            type: "get",
            data: {
                "college": Number($(this).val())
            },
            success: function (data) {
                for (var i = -1; i < data["data"].length; i++) {
                    if (i == -1) {
                        $("#specialty-select").append("<option value='' selected hidden>选择专业</option>");
                    } else {
                        $("#specialty-select").append("<option value=" + data['data'][i]['id'] + ">" + data['data'][i]['name'] + "</option>");
                    }
                }
            }
        })
    })
});
//判断浏览器是否支持FileReader接口
if (typeof FileReader == 'undefined') {
    document.getElementById("xmTanDiv").InnerHTML = "<h1>当前浏览器不支持FileReader接口</h1>";
    //使选择控件不可操作
    document.getElementById("xdaTanFileImg").setAttribute("disabled", "disabled");
}

//选择图片，马上预览
function xmTanUploadImg(obj) {
    var file = obj.files[0];

    // console.log(obj);
    // console.log(file);
    // console.log("file.size = " + file.size);  //file.size 单位为byte
    if (file.size <= 524288) {
        var reader = new FileReader();
        //读取文件过程方法
        // reader.onloadstart = function (e) {
        //     console.log("开始读取....");
        // };
        // reader.onprogress = function (e) {
        //     console.log("正在读取中....");
        // };
        // reader.onabort = function (e) {
        //     console.log("中断读取....");
        // };
        // reader.onerror = function (e) {
        //     console.log("读取异常....");
        // };
        reader.onload = function (e) {
            // console.log("成功读取....");
            var img = document.getElementById("xmTanImg");
            $(".preview-picture").css("display", "block");
            $(".head-content").css("height", "600px");
            img.height = "284";
            img.width = "284";
            img.src = e.target.result;
            //或者 img.src = this.result;  //e.target == this
        };
        reader.readAsDataURL(file)
    } else {
        $("input[name='head-picture']").val("");
        alert("图片不能大于512KB");
    }
}
