
% rebase('layout.tpl', mensajeBienvenida=mensajeBienvenida, TituloMenu=TituloMenu,SubtituloMensaje=SubtituloMensaje,IDConfiguracion=IDConfiguracion,ImagenLogin=ImagenLogin,IconoLogin=IconoLogin)

 <div class="container-fluid">
     <div class="row">
      <div class="col-7">

        <div class="col-12">
          <img class="img-fluid" style="overflow: hidden;" src="{{ImagenLogin}}" />
        </div>
       
      </div>

      <div class="col-5" style="align-items: center;"> 
         <div style="text-align: center;">
        <img style="
        object-fit: contain;
        margin-top: 90px;
        width: 270px;
        height: 223px;
        " src="{{IconoLogin}}"/>
        </div>
        
        <div class="col-12" style="align-items: center;">
            <h3 style="color:#1A5632;font: normal normal medium 40px/47px Rubik; text-align: center;">{{TituloMenu}}</h3>
        </div>
  
        <div class="col-12 mt-3">
            <p style="text-align: center;
            font: normal normal normal 20px/24px Rubik;
            letter-spacing: 0px;
            color: #1A5632;
            opacity: 1;">{{SubtituloMensaje}}</p>
        </div>

        <div class="col-12 mt-2">
          <div style="text-align:center">
           <a href="/login" class="btn btn-success mt-3" style="text-align: center; width: 350px; background-color: #1A5632; padding: 9px; font-weight: 500;">Ingresa ahora</a>
           </div>
        </div>
      </div> 
     </div>

   </div>


