function login() {
            // console.log($("#login_form").serializeJSON())
            $.ajax({
                type:"POST",
                url:"/user/login",
                dataType:"json",
                data:$("#login_form").serialize(),
                success:function (data) {
                    if (data.success){
                        window.location=data.path
                        alert(data.success);
                    }else {
                        alert(data.error);
                    }

                }
            })
        }