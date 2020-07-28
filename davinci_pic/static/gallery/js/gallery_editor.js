$(document).ready(function(){

  var dom = $(".row_vault_add_col").find("input[type='checkbox']");
  for(var i=0; i<dom.length; i++){
      dom[i].checked = false;
  }
    

    $("#delete-image-id").click(function(){
     $(".without-edit").removeClass("div-display");
     $(".without-edit").addClass("div-hide");
     $(".with-edit").removeClass("div-hide");
     $(".with-edit").addClass("div-display");

    });


    $(".folder-name-img-wrap-with-edit").click(function(){
      
      $(this).find('input[type="checkbox"]').click();

    });

    $(".file-name-img-wrap-with-edit").click(function(){
      
      $(this).find('input[type="checkbox"]').click();

    });



    $("#delete-selected-image-id").click(function(){
      $(".with-edit").removeClass("div-display");
      $(".with-edit").addClass("div-hide");
      $(".without-edit").removeClass("div-hide");
      $(".without-edit").addClass("div-display");
      
     const dom_node =  document.querySelectorAll('#row-for-files input[type="checkbox"]');
     var arr = ""
     
     for (var i = 0; i < dom_node.length; i++) {
      if(dom_node[i].checked == true){
        var type = dom_node[i].parentElement.className.split("-")[0];
        if(type=="folder"){
          arr = arr.concat(type,"/",dom_node[i].id,"**")
        }
        else if(type=="file"){
          arr = arr.concat(type,"/",dom_node[i].id,"**")
        }
      
        
        
      }
    }

   
      
        console.log(arr);


        var csrftoken = Cookies.get('csrftoken');
        
        $.ajax({
                  url: '/davinci/gallery/vault/edit_files/',
                  type: 'POST',
                  data: {
                    'object': arr,
                    'function': "delete",
                    'path': window.location.href,
                  },
                  headers: { "X-CSRFToken": csrftoken },
                  dataType: 'json',
                  success: function(data) {
                            if(data.status!= undefined && data.status!= null){
            
                            
                              console.log(data)
                              window.location.href = window.location.href
                            }
                            else{
                              console.log('failed');
            
                            }
                  }
            
            
               });
              
     
    
 
     });


     $("#cancel-delete").click(function(){
      $(".with-edit").removeClass("div-display");
      $(".with-edit").addClass("div-hide");
      $(".without-edit").removeClass("div-hide");
      $(".without-edit").addClass("div-display");
 
     });

     $("#rename-file-id").click(function(){
      $(".without-edit").removeClass("div-display");
      $(".without-edit").addClass("div-hide");
      $(".with-edit-rename").removeClass("div-hide");
      $(".with-edit-rename").addClass("div-display");
 
     });

     $("#back-main").click(function(){
      $(".with-edit-rename").removeClass("div-display");
      $(".with-edit-rename").addClass("div-hide");
      $(".without-edit").removeClass("div-hide");
      $(".without-edit").addClass("div-display");
 
     });

     $("#cancel-rename").click(function(){
      $(".with-edit-rename").removeClass("div-display");
      $(".with-edit-rename").addClass("div-hide");
      $(".without-edit").removeClass("div-hide");
      $(".without-edit").addClass("div-display");
 
     });


     $(".with-edit-rename .folder-class-with-edit-rename").click(function(){

      var val = prompt("Enter name");
      if(val == null || val == ""){
        console.log("cancelled");
      }
      else{

         var old_name = $(this).find(".folder-name")[0].innerText;
         var name_string = old_name.concat("**",val);
         console.log(val);

        var csrftoken = Cookies.get('csrftoken');
        
        $.ajax({
                  url: '/davinci/gallery/vault/edit_files/',
                  type: 'POST',
                  data: {
                    'object': name_string,
                    'function': "rename_folder",
                    'path': window.location.href,
                  },
                  headers: { "X-CSRFToken": csrftoken },
                  dataType: 'json',
                  success: function(data) {
                            if(data.status!= undefined && data.status!= null){
            
                            
                              console.log(data)
                              window.location.href = window.location.href
                            }
                            else{
                              console.log('failed');
            
                            }
                  }
            
            
               });
              
      }
      
     });

     $(".with-edit-rename .file-class-with-edit-rename").click(function(){

      var val = prompt("Enter name");
      var old_name = $(this).find(".file-name")[0].innerText;
      arr_old = old_name.split(".");
      if(val != null && val != ""){
        arr_new = val.split(".");
      }
      
      if(val == null || val == ""){
        console.log("cancelled");
      }
      else if(arr_new[arr_new.length-1] != arr_old[arr_old.length-1]){

         alert("wrong extension")
      }
      else{

         var old_name = $(this).find(".file-name")[0].innerText;
         var name_string = old_name.concat("**",val);
         console.log(val);

        var csrftoken = Cookies.get('csrftoken');
        
        $.ajax({
                  url: '/davinci/gallery/vault/edit_files/',
                  type: 'POST',
                  data: {
                    'object': name_string,
                    'function': "rename_file",
                    'path': window.location.href,
                  },
                  headers: { "X-CSRFToken": csrftoken },
                  dataType: 'json',
                  success: function(data) {
                            if(data.status!= undefined && data.status!= null){
            
                            
                              console.log(data)
                              window.location.href = window.location.href
                            }
                            else{
                              console.log('failed');
            
                            }
                  }
            
            
               });
              
      }
      
     });
     
     

    $('#add-folder-id').click(function(){
        
        // var val = '<div class="col-md-3"> <img src="/static/gallery/images/folder-icon.png" width="200px" alt="folder"> </div>'
        var csrftoken = Cookies.get('csrftoken');
        var folder_name = prompt("Folder name","newfolder")
        
        if(folder_name != null){
        $.ajax({
                  url: '/davinci/gallery/vault/add_files/',
                  type: 'POST',
                  data: {
                    'folder_name': folder_name,
                    'data_base64': " ",
                    'path': window.location.href,
                  },
                  headers: { "X-CSRFToken": csrftoken },
                  dataType: 'json',
                  success: function(data) {
                            if(data.val!= undefined && data.val!= null){
            
                              $('#row-for-files').append(data.val)
                              console.log(data.folder_name)
                              window.location.href = window.location.href
                            }
                            else{
                              console.log('failed');
            
                            }
                  }
            
            
               });
              }
    });

// $(".folder-name-img-wrap").click(function(){


// });

$(".folder-class").click(function(){
var temp = $(this).find(".folder-name").text();
var id_temp = $(this).attr("id");
var formatted_name = ""
for(i=0;i<temp.length;i++){
  if(temp[i] != " "){
    formatted_name = formatted_name.concat(temp[i])
    
    
}
}

if(window.location.href[window.location.href.length-1] == '/'){
window.location.href = window.location.href + id_temp;
}
else{
  window.location.href = window.location.href+"/" + id_temp;
}

});

$("#add-image-id").click(function(){

  document.getElementById("file-input").click();

});
$('#file-input').change(function(e){

  if(e.target.files[0].type.split("/")[0]=="image"){
   
    var file = e.target.files[0];
    function readRecord(file) {
      return new Promise(function(resolve, reject) {
        
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function(event) {
            var obj = reader.result
            resolve(obj);
        };
      });
    };
    
    
    readRecord(file).then(function(obj) {
     console.log(obj);
    
    var csrftoken = Cookies.get('csrftoken');

    $.ajax({
      url: '/davinci/gallery/vault/add_files/',
      type: 'POST',
      data: {
        'folder_name': file.name,
        'data_base64': obj,
        'path': window.location.href,
      },
      headers: { "X-CSRFToken": csrftoken },
      dataType: 'json',
      success: function(data) {
                if(data.val!= undefined && data.val!= null){

                  // $('#row-for-files').append(data.val)
                  // console.log(data.folder_name)
                  console.log("success");
                  window.location.href = window.location.href;
                }
                else{
                  console.log('failed');

                }
      }


   });  
   //end of ajax


}); //end of thenfunction

    console.log(e.target.files[0]);
  }
  else{
    console.log("not image")
  }
 

});

$(".file-name-img-wrap").click(function(){

  var img = $(this)[0].firstElementChild;
  console.log(img.src);
  $("#image_full_view_vault").attr("src",img.src);
  $(".image_fullscreen_vault").removeClass("div-hide");

});

$("#icon-close_vault").click(function(){

  $(".image_fullscreen_vault").addClass("div-hide");     

});



$(".collage-mode-select").click(function(){
  var layout = $(this).attr("id");

  layout = layout.concat("-","class");   

  window.location.href = "http://"+ window.location.hostname +"/davinci/gallery/edit/root/collage/"+ layout;





});

$(".making-collage-section").load(function(){

  var arr = window.location.href.split("?")[1];
  




});

$("#go-back-mode").click(function(){

  
  
  
  $("#layout-icon").find("img").remove();
  window.location.href = "http://"+ window.location.hostname +"/davinci/gallery/edit/root/";
  

});

$("#go-back-main").click(function(){

  $("#layout-icon").find("img").remove();

  window.location.href = "http://"+ window.location.hostname +"/davinci/gallery/";
});



$("#adding_to_collage").click(function(){

 
  $("#files_for_collage").click();
  
  
 

});
$('#files_for_collage').change(function(e){
  for(var i = 0; i<e.target.files.length;i++){

  
  if(e.target.files[i].type.split("/")[0]=="image"){
   
    var file = e.target.files[i];
    console.log(e.target.files);
    function readRecord(file) {
      return new Promise(function(resolve, reject) {
        
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function(event) {
            var obj = reader.result;
            id_for_preview = file.name;
            var html_code=  '<div class="col-md-2 image-previews"><img src="" alt="img-preview" id="'+id_for_preview+'"></div>';
            $(".row_for_preview").append(html_code);
            var img = document.getElementById(id_for_preview);
            img.src = reader.result;
            
        };
      });
    };
    
    
    readRecord(file);
  }
}

});



function dataURLtoFile(dataurl, filename) {
  var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
      bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
      while(n--){
          u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], filename, {type:mime});
  }



$("#make-collage").click(function(){



var mode = window.location.href.split("/")
mode = mode[mode.length-2] 
console.log("mode",mode);
var layout_no = 4
if(mode == "tile_9-class"){

  layout_no = 9
} 
else if(mode == "tile_5-class"){

  layout_no = 5

}else{

  layout_no = 4
}
console.log("layoutno",layout_no)
  
var obj = ""  
var file_arr = $("#files_for_collage")[0];
console.log(file_arr);
var l = file_arr.files.length;
if(l == 0){

  var img = $(".row_for_preview").find("img");
  l = img.length;
  var file_img;
  file_arr = {'files':[]}
  for(var j=0;j<l;j++){
    file_img = dataURLtoFile(img[j].src, j.toString() + '.png');
      file_arr.files.push(file_img)


  }
   
}
var file;
var data = new FormData();
if(l == layout_no){
  for(var i=0;i<l;i++){
    count = i+1
     file = file_arr.files[i];
     console.log(file)
     data.append(count.toString(), file);

  }
  data.append("path_url",window.location.href)
  
  
  
 
  var csrftoken = Cookies.get('csrftoken');
  
    $.ajax({
      url: '/davinci/gallery/edit/root/collage/0/',
      type: 'POST',
      processData : false,
      contentType : false,
      data: data,
      headers: { "X-CSRFToken": csrftoken },
      dataType: 'json',
      success: function(data) {
                if(data.val!= undefined && data.val!= null){

                  // $('#row-for-files').append(data.val)
                  // console.log(data.folder_name)
                  console.log("success");
                  
                  // url_ = data.url_output.slice(2,)
                  url_ = data.url_output
                  console.log(url_)
                
                  $("#final_image").attr("src",url_);
                  $("#image_full_view").attr("src",url_);
                  download_url = document.getElementById("final_image").src;
                  $("#final_image_download").attr("href",download_url);
                  $(".row_download").removeClass("div-hide");
                  $(".row_for_preview").find(".image-previews").remove();
                  
                }
                else{
                  console.log('failed');

                }
      }


   });  

}
else{
  alert("Insert Required amount of images");
  window.location.href = window.location.href
}

});

$("#final_image").click(function(){

    $(".image_fullscreen").removeClass("div-hide");

});

$("#icon-close").click(function(){

  $(".image_fullscreen").addClass("div-hide");     

});

$(".row_vault_add_col").click(function(){

  $(this).find('input[type="checkbox"]').click();

});

$(".row_vault_add_col").find('input[type="checkbox"]').click(function(){

$(this).click();
});

function check_click(){

  $(".row_vault_add_col").click(function(){

    $(this).find('input[type="checkbox"]').click();

  });

  $(".row_vault_add_col").find('input[type="checkbox"]').click(function(){

  $(this).click();
  });

} 


$("#adding_to_collage_from_vault").click(function(){

   $(".add-vault").removeClass("div-hide");
   $(".row_vault_add").find(".row_vault_add_col").remove();

   var csrftoken = Cookies.get('csrftoken');
  
        
        $.ajax({
                  url: '/davinci/gallery/edit/root/collage_load/load_vault/',
                  type: 'POST',
                  data: {
                    'object': 10,
                    'path': window.location.href,
                  },
                  headers: { "X-CSRFToken": csrftoken },
                  dataType: 'json',
                  success: function(data) {
                            if(data.val!= undefined && data.val!= null){

                              var filename = data.filename.split("::")
                              var url_output = data.url_output.split("**")
                              l = data.count
                              for(var i=0; i<l; i++){

                              var fname = filename[i].split("**")[0]

                              fname = "add-"+fname +"_" + i.toString();
                              var html_code = '<div class="col-md-4 row_vault_add_col" id="'+fname +'"><input type="checkbox"/><img src="'+ url_output[i]+'" alt="image_full_view" class="img-thumbnail"></div>'
            
                             
                              $(".row_vault_add").append(html_code);

                              }
                              check_click();
                             
                            }
                            else{
                              console.log('failed');
            
                            }
                  }
            
            
               }); //end of ajax

              

});








$("#add-vault-close-btn").click(function(){

  $(".add-vault").addClass("div-hide");
  var dom = $(".row_vault_add_col").find("input[type='checkbox']");
  for(var i=0; i<dom.length; i++){
      dom[i].checked = false;
  }
  
  $(".row_vault_add").find(".row_vault_add_col").remove();

});

$("#add-vault-btn-cancel").click(function(){

  $(".add-vault").addClass("div-hide");
  var dom = $(".row_vault_add_col").find("input[type='checkbox']");
  for(var i=0; i<dom.length; i++){
      dom[i].checked = false;
  }  

  $(".row_vault_add").find(".row_vault_add_col").remove();

});


$("#add-vault-btn-add").click(function(){

  // $("#loading").removeClass("div-hide");

  var dom = $(".row_vault_add_col").find("input[type='checkbox']");
  var img_arr = []
  var arr = []
  var l = dom.length;
  for(var i=0; i<l; i++){
    if(dom[i].checked == true){
      arr.push(dom[i].parentElement.id);
      var temp = dom[i].nextElementSibling;
      img_arr.push(temp);
    }
  }

var mode = window.location.href.split("/")
mode = mode[mode.length-2] 
var layout_no = mode.split("-")[0];
layout_no = layout_no.split("_")[1]
if(layout_no == "9"){

  layout_no = 9
} 
else if(layout_no == "5"){

  layout_no = 5

}else{

  layout_no = 4
}
if(arr.length == layout_no){
  

    
  var l = arr.length

  for(var j=0; j<l; j++){

  id_for_preview = "preview-" + arr[j].split("-")[1];
  
  var html_code=  '<div class="col-md-2 image-previews"><img src="" alt="img-preview" id="'+id_for_preview+'"></div>';
  $(".row_for_preview").append(html_code);
  var img_element = document.getElementById(id_for_preview);
  // img.src = img_arr[j];
  
  
  var c = document.createElement('canvas');
  var img = img_arr[j];
  c.height = img.naturalHeight;
  c.width = img.naturalWidth;
  var ctx = c.getContext('2d');

  ctx.drawImage(img, 0, 0, c.width, c.height);
  var base64String = c.toDataURL();
  img_element.src = base64String;
  
  // data:image/png;base64,

  
  }

  $(".add-vault").addClass("div-hide");
   
  

  var dom = $(".row_vault_add_col").find("input[type='checkbox']");
  for(var i=0; i<dom.length; i++){
      dom[i].checked = false;
  } 

}
else{
  alert("Select required amount");
}
// $("#loading").addClass("div-hide");

});


$(".col_for_format_selection").click(function(){
  
  var id_format = $(this)[0].id.split("_")[0];
  
  if(window.location.href[window.location.href.length-1] == '/'){
    window.location.href = window.location.href + id_format;
    }
    else{
      window.location.href = window.location.href+"/" + id_format;
    }

});

$("#format-image-browse-btn").click(function(){

  $(".row_imgconv_preview").find(".col_imgconv_preview").remove();

$("#format-image-browse-input").click();

});


$('#format-image-browse-input').change(function(e){


if(e.target.files.length <= 5) {




for(var i = 0; i<e.target.files.length;i++){



  
  if(e.target.files[i].type.split("/")[0]=="image"){
   
    var file = e.target.files[i];
    console.log(e.target.files);
    function readRecord(file) {
      return new Promise(function(resolve, reject) {
        
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function(event) {
            var obj = reader.result;
            id_for_preview = file.name;
            $(".col_imgconv_preview_sample").addClass("div-hide");
            var html_code=  '<div class="col-md-2 col_imgconv_preview"><img src="" alt="img-preview" id="'+id_for_preview+'"></div>';
            $(".row_imgconv_preview").append(html_code);
            var img = document.getElementById(id_for_preview);
            img.src = reader.result;
            
        };
      });
    };
    
    
    readRecord(file);
  }
}

}

else{
  alert("Maximum 5 files!");
}

});

$("#format-image-convert-btn").click(function(){

  $("#format-convert-submit").click();
  
  

});



}); //end of whole function