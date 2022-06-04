const RUTAS = {
    'admin':{'admin':'HomeADMIN.html'},
    'user':{'user':'HomeUSER.html'}
}
function initButton(){
    $('#submitButtonID').on('click',()=>{

        let user = $('#username').val()
        let pass = $('#password').val()
        let ruta = undefined;

        if(user && pass)
            ruta = RUTAS[user][pass];

        if(ruta){
            //window.location.href = ruta;
           // alert('que asco de vida')
           window.localStorage.setItem('user', user)
           window.location.assign('Home.html')    
           //document.getElementById('View_all_videos').remove()     
            return false;
        }else{
            alert('login incorrecto')
        }
    });
}

initButton();