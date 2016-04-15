if (window.WebSocket != undefined) {
    // WebSocket
    var API = {
        msg: {
            date: Date.now(),
            command: "command",
            content: "content"
        },
        createNew: function() {
            // var ws = {};
            ws = new WebSocket("ws://localhost:8888/api");
            ws.onopen = function(evt) {
                console.log("WebSocket connected.");
                switch (window.location.pathname) {
                    case "/setting":
                        API.msg.command = "douban_captcha";
                        api.sendmsg();
                        break;
                    case "/fm":
                        API.msg.command = "douban_fav_channels";
                        
                        break;
                    default:
                        break;
                };
            };
            ws.sendmsg = function() {
                API.msg.date = Date.now();
                console.log(JSON.stringify(API.msg));
                api.send(JSON.stringify(API.msg));
            };
            ws.onmessage = function(evt) {
                result = JSON.parse(evt.data);
                switch (result.command) {
                    case "douban_captcha":
                        document.getElementById('captcha').src = result.content;
                        break;
                    case "douban_login":
                        if (result.content[0]){
                            alert("登录成功");
                        } else {
                            alert("登录失败",result.content[1]);
                        }
                        break;
                    case "douban_fav_channels":
                        break;
                    default:
                        break;
                }
                return true;
            };
            ws.onclose = function() {
                console.log("WebSocket closed.");
            };
            return ws;
        }
    };
    (function() {
        document.addEventListener("DOMContentLoaded", function() {
            //init websocket
            var api = API.createNew();

            /* menu toggle function*/
            if (document.getElementById('menu_toggle') != undefined) {
                document.getElementById('menu_toggle').addEventListener("click", function() {
                    document.getElementById('nav').classList.toggle('nav-toggle');
                    document.getElementById('layout').classList.toggle('layout-toggle');
                });
            }

            /*douban login function*/
            if (document.getElementById('douban_login') != undefined) {
                document.getElementById('douban_login').addEventListener("click", function() {
                    api.msg = {
                        command: "douban_login",
                        content: {
                            username: document.getElementById('douban_email').value,
                            password: document.getElementById('douban_passwd').value,
                            captcha_solution: document.getElementById('douban_captcha').value,
                            captcha_id: document.getElementById('captcha').src.split('=')[2]
                        }
                    }
                    api.sendmsg();
                });
            }

        })
    }());

}

function fm() {

};
