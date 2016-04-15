if (window.WebSocket != undefined) {
    (function() {
        document.addEventListener("DOMContentLoaded", function() {
            ws = new WebSocket("ws://localhost:8888/api");

            ws.onopen = function(evt) {
                var msg = {
                    time: Date.now(),
                    command: "douban_captcha",
                    content: ""
                }
                ws.send(JSON.stringify(msg));
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
                }
            }

            document.getElementById('douban_login').addEventListener("click",function(){
                var msg = {
                    date: Date.now(),
                    command: "douban_login",
                    content: {
                        username : document.getElementById('douban_email').value,
                        password : document.getElementById('douban_passwd').value,
                        captcha_solution : document.getElementById('douban_captcha').value,
                        captcha_id : document.getElementById('captcha').src.split('=')[2]
                    }
                }
                ws.send(JSON.stringify(msg));
            });

        })
    }());

}
