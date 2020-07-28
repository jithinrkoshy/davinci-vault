from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.cache import cache_control
from davinci.models import USER_DATA
from davinci.models import folder_files_model
from davinci.forms import USER_DATA_FORM
import os
from django.contrib.auth.models import User
import pandas as pd
import pickle as pk
from django.contrib.sites.shortcuts import get_current_site
import base64 
from references.tile_4 import tile_4
from references.tile_5 import tile_5
from references.tile_9 import tile_9
from glob import glob
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image


# Create your views here.

class Treenode:
    def __init__(self,node_name):
        self.node_name = node_name
        self.folder_id = None
        self.children = []
        self.parent = None

    def add_child(self,child):
        child.parent = self
        self.children.append(child)

def search_node(request,node,item,node_return=None,flag=-1):    #name of item is passed
    path = "./static/gallery/data/"+ str(request.user.username)
    with open(path+"/"+str(request.user.username)+".pickle","rb") as f_obj_read:
        root = pk.load(f_obj_read)    
    if(node.folder_id == item):
        print("returning node")
        node_return = node
        flag=1
        return node_return,flag  
    for child in node.children:
        if(flag==1):
            return node_return,flag
        node_return,flag = search_node(request,child,item,node_return,flag)
        
    print("returning none")
    return node_return,flag



def index(request):
    form = UserCreationForm()
    register = False
    if request.method == 'POST':
          form =  UserCreationForm(request.POST)
          

          if form.is_valid():
              user = form.save()
              user_obj = User.objects.get(username=user.username)
              userdata = USER_DATA.objects.create(user_id =user_obj, username = user.username,login_count = 0)
              ffm = folder_files_model.objects.create(user_id =user_obj, username = user.username,folder_count = 0,files_count=0)
              path = os.path.join("./static/gallery/data/",user.username)
              os.mkdir(path)
              os.mkdir(path+"/media")
              os.mkdir(path+"/media/output")
              root = Treenode(str(user.username))
              root.folder_id = "root$$" + str(user.username)
              with open(path+"/"+str(user.username)+".pickle","wb") as f_obj_write:
                     pk.dump(root,f_obj_write, protocol=pk.HIGHEST_PROTOCOL)
              register = True
              data = {'register':register}
              form = UserCreationForm()
              return JsonResponse(data)
          else:
              err = " "
              for i in form.errors:
                  err+=str(form.errors[i])
              data = {'register':register,'error':err}
              print(form.error_messages)
              return JsonResponse(data)    


    return render(request,'davinci/index.html',context = {'reg_form': form,'register':register})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                userdata = USER_DATA.objects.get(username = user.username)
                if(userdata.login_count!=0):
                   userdata.login_count+=1
                userdata.save()
                return redirect("davinci:gallery")
            else: 
                return redirect("index")
    
    return redirect("index")            

    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/davinci/sign_in/')
def gallery(request):
    userdata = USER_DATA.objects.get(username = request.user.username)
    pk=userdata.username
    cnt=userdata.login_count
    if(int(cnt)==0):
       userdata.login_count+=1
       userdata.save()
       return redirect("davinci:info")
    else:    
       return render(request,'davinci/gallery.html',context={'pk':pk})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/davinci/sign_in/')
def info_request(request):
    userdata = USER_DATA.objects.get(username = request.user.username)
    if request.method == 'POST':
        form =  USER_DATA_FORM(request.POST,instance = userdata)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            return redirect("davinci:gallery")

    form = USER_DATA_FORM(initial={'email':userdata.email,
    'first_name':userdata.first_name,'last_name':userdata.last_name,
    'country_code':userdata.country_code,'mobile_number':userdata.mobile_number})
    if(userdata.email == None):
          dash_cnt = '0'
    else:
        dash_cnt = userdata.login_count      
    dictionary = {'pk':userdata.username,'form':form,'cnt':dash_cnt}    
    return render(request,'davinci/info_signin.html',context=dictionary)    



def logout_request(request):
    logout(request)
    return redirect('index') 


def print_tree(node):
    print(node.node_name)
    for child in node.children:
        print_tree(child)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/davinci/sign_in/')
def vault_request(request):
        
    abs_path = str(request.get_full_path()).split("/")
    rel_url_start = abs_path.index("root")
    abs_path = abs_path[int(rel_url_start)+1:len(abs_path)]
    
    userdata = USER_DATA.objects.get(username = request.user.username)
    p_key=userdata.username
    path_for_user = "./static/gallery/data/"+ str(request.user.username) 
    
    with open(path_for_user+"/"+str(request.user.username)+".pickle","rb") as f_obj_read:
        root = pk.load(f_obj_read)    
    
    node = root
    if(len(abs_path)==1 and abs_path[0] == ''):
        print("it is root")
        folder_list = root.children
        
    else:
        
        for i in range(0,len(abs_path)):
            
            node,flag = search_node(request,node,str(abs_path[i]))
            if(node == None):
                html_array = []
                print("returning none and search failed")
                return render(request,'davinci/vault.html',context={'pk':p_key,'folder_data':html_array }) 
        folder_list = node.children
        print(node.node_name) 

    html_array_folders = []  
    html_array_files = []        
    for i in folder_list:
        temp = i
        if(temp.node_name.split("/")[0]=="folder"):
            id_for_dom = temp.folder_id
            
            formatted_folder_name = temp.node_name.split("/")[1]
            data = (id_for_dom,formatted_folder_name)
            
            html_array_folders.append(data)

        elif(temp.node_name.split("/")[0]=="file"):
            file_name = temp.node_name.split("/")[1]
            path_for_files = "/static/gallery/data/"+ str(request.user.username) 
            url = path_for_files + "/" + str(node.folder_id) + "**"+ file_name
            # print("this is url:"+url)
            data = (file_name,url)
            html_array_files.append(data)
   
    # print(html_array)
    return render(request,'davinci/vault.html',context={'pk':p_key,'folder_data':html_array_folders,'folder_files':html_array_files })    

def print_tree(node):
    print(node.node_name)
    for child in node.children:
        print_tree(child)


def add_files(request):
    
    path = "./static/gallery/data/"+ str(request.user.username)
    with open(path+"/"+str(request.user.username)+".pickle","rb") as f_obj_read:
            root = pk.load(f_obj_read)  
       
    
      
    abs_path = str(request.POST['path']).split("/")
    
    rel_url_start = abs_path.index("root")
    abs_path = abs_path[int(rel_url_start)+1:len(abs_path)]
    node = root
   

    
    if(abs_path[0]!=''):
        for i in range(0,len(abs_path)):
            node,flag = search_node(request,node,str(abs_path[i]))
            if(node == None):
                print("current directory not found in tree")
                data = {'val':"",'folder_name':""}
                return JsonResponse(data)

    data_base64 = request.POST['data_base64']
    if(data_base64 != " "):
        index_base64 = int(data_base64.find("base64"))
        data_base64 = data_base64[index_base64+7:]
        
        imgdata = base64.b64decode(data_base64)
        filename = request.POST['folder_name']
        filename = "file/"+ filename
        counter_name = 0
        for i in range(len(node.children)):
            if(node.children[i].node_name == str(filename)):
                print("file exists")
                counter_name +=1
                filename_1 = filename.split(".")[0]
                filename_2 = filename.split(".")[1]
                if(counter_name >=2 ):
                    filename_1 = filename_1[0:-3]
                filename = filename_1 + "("+str(counter_name) + ")" + "." + filename_2
                i=-1
        
        new_child = Treenode(str(filename))       
        node.add_child(new_child)        
        print_tree(root)
        with open(path+"/"+str(request.user.username)+".pickle","wb") as f_obj_write:
            pk.dump(root,f_obj_write, protocol=pk.HIGHEST_PROTOCOL)
        
        save_filename = str(node.folder_id)+"**"+filename.split("/")[1] 
        
        print(save_filename)         
        with open(path +"/"+ save_filename , 'wb') as f:
            f.write(imgdata)
        data = {'val':"",'folder_name':""}
        return JsonResponse(data)            
            
    folder_name = request.POST['folder_name']
    
    ffm = folder_files_model.objects.get(username = request.user.username)       
    folder_id = ffm.folder_count
    folder_id +=1
    ffm.folder_count = folder_id
    ffm.save()
    id_for_dom = "folder_id_"+str(folder_id)       
    

    if(str(folder_name) == 'newfolder'):
       formatted_folder_name = str(folder_name)+str(folder_id)
    else:
        formatted_folder_name = str(folder_name)
    for i in node.children:
        if(i.node_name == "folder/"+str(formatted_folder_name)):
            print("folder exists")
            data = {'val':"",'folder_name':""}
            return JsonResponse(data)
    s_item = "folder/"+str(formatted_folder_name)        
    new_child = Treenode(s_item)
    

    new_child.folder_id = id_for_dom        
    node.add_child(new_child)        
    print_tree(root)
    with open(path+"/"+str(request.user.username)+".pickle","wb") as f_obj_write:
            pk.dump(root,f_obj_write, protocol=pk.HIGHEST_PROTOCOL) 
    html_val = '<div id="'+ str(id_for_dom)+'" class="col-md-3 folder-class"><div class="folder-name-img-wrap"> <img src="/static/gallery/images/folder-icon.png" alt="folder"><div class="folder-name">'+str(formatted_folder_name)+'</div></div>  </div>' 

    data = {'val':html_val,'folder_name':formatted_folder_name}
    return JsonResponse(data)



def edit_files(request):
    obj = request.POST["object"]
    func = request.POST["function"]
    
    if(func == "delete"):
        path = "./static/gallery/data/"+ str(request.user.username)
        with open(path+"/"+str(request.user.username)+".pickle","rb") as f_obj_read:
            root = pk.load(f_obj_read)  
        
    
      
        abs_path = str(request.POST['path']).split("/")
        
        rel_url_start = abs_path.index("root")
        abs_path = abs_path[int(rel_url_start)+1:len(abs_path)]
        node = root

        if(abs_path[0]!=''):
            for i in range(0,len(abs_path)):
                node,flag = search_node(request,node,str(abs_path[i]))
                if(node == None):
                    print("current directory not found in tree")
                    data = {'status':"failed"}
                    return JsonResponse(data)
        
        array_obj = obj.split("**")[0:-1]
        
        new_child_array = []
        for i in array_obj:
            for j in node.children:
                if(j.node_name != i):
                    new_child_array.append(j)
                elif(j.node_name == i):
                    old_node = j    
                

            if(i.split("/")[0]=="folder"):
                
                pickle_file = str(request.user.username)+".pickle"
                dirs = os.listdir(path+"/")
                dirs.remove(pickle_file)
                dirs.remove("media")
                for k in dirs:
                    if(k.split("**")[0] == old_node.folder_id):
                        os.remove(path+"/"+k)


            if(i.split("/")[0]=="file"):
                
                save_filename = str(node.folder_id)+"**"+i.split("/")[1]  
                os.remove(path+"/"+save_filename) 

            node.children =  new_child_array
            new_child_array = [] 
                  
        with open(path+"/"+str(request.user.username)+".pickle","wb") as f_obj_write:
            pk.dump(root,f_obj_write, protocol=pk.HIGHEST_PROTOCOL)
  

        data = {'status':"success"}
        return JsonResponse(data)

    elif(func == "rename_folder"):
        
        path = "./static/gallery/data/"+ str(request.user.username)
        with open(path+"/"+str(request.user.username)+".pickle","rb") as f_obj_read:
            root = pk.load(f_obj_read)  
       
    
      
        abs_path = str(request.POST['path']).split("/")
        
        rel_url_start = abs_path.index("root")
        abs_path = abs_path[int(rel_url_start)+1:len(abs_path)]
        node = root

        if(abs_path[0]!=''):
            for i in range(0,len(abs_path)):
                node,flag = search_node(request,node,str(abs_path[i]))
                if(node == None):
                    print("current directory not found in tree")
                    data = {'status':"failed"}
                    return JsonResponse(data)

        old_name = request.POST["object"].split("**")[0]   
        new_name = request.POST["object"].split("**")[1]
        flag = 0
        for i in range(len(node.children)):
            if(node.children[i].node_name == "folder/" +new_name):
                flag += 1
                new_name = new_name + "("+ str(flag) +")"
                i=-1
        
        
        for k in node.children:
            if(k.node_name == "folder/"+old_name):
                old_node = k

        for i in node.children:
            if(i.node_name == "folder/"+old_name):
               i.node_name =   "folder/"+new_name  

        with open(path+"/"+str(request.user.username)+".pickle","wb") as f_obj_write:
            pk.dump(root,f_obj_write, protocol=pk.HIGHEST_PROTOCOL)                  
        data = {'status':"success"}
        return JsonResponse(data)

    elif(func == "rename_file"):
        
        path = "./static/gallery/data/"+ str(request.user.username)
        with open(path+"/"+str(request.user.username)+".pickle","rb") as f_obj_read:
            root = pk.load(f_obj_read)  
       
    
      
        abs_path = str(request.POST['path']).split("/")
        
        rel_url_start = abs_path.index("root")
        abs_path = abs_path[int(rel_url_start)+1:len(abs_path)]
        node = root

        if(abs_path[0]!=''):
            for i in range(0,len(abs_path)):
                node,flag = search_node(request,node,str(abs_path[i]))
                if(node == None):
                    print("current directory not found in tree")
                    data = {'status':"failed"}
                    return JsonResponse(data)

        old_name = request.POST["object"].split("**")[0]   
        new_name = request.POST["object"].split("**")[1]

        flag = 0
        count=0
        for i in range(len(node.children)):
            if(node.children[i].node_name == "file/" +new_name):
                flag += 1
                count+=1
                if(count==1):
                    new_name = new_name.split(".")[0] + "("+ str(flag) +")" + "." + new_name.split(".")[1]
                else:
                    name_o = new_name.split(".")[0]
                    for k in range(len(name_o)-1,-1,-1):
                        if(name_o[k] == "("):
                            ind_br = k
                            break
                    name_o = name_o[0:ind_br+1] + str(flag) + ")"
                    new_name =  name_o + "." + new_name.split(".")[1]
                i=-1

        pickle_file = str(request.user.username)+".pickle"
        dirs = os.listdir(path+"/")
        dirs.remove(pickle_file)
        
        for i in dirs:
            if(i.split("**")[0] == node.folder_id):
                if(i.split("**")[-1]==old_name):
                    save_filename = node.folder_id + "**" +  new_name
                    os.rename(path+"/"+i, path + "/" +save_filename)

        for i in node.children:
            if(i.node_name == "file/"+old_name):
               i.node_name =   "file/"+new_name  

        with open(path+"/"+str(request.user.username)+".pickle","wb") as f_obj_write:
            pk.dump(root,f_obj_write, protocol=pk.HIGHEST_PROTOCOL)                  
        data = {'status':"success"}
        return JsonResponse(data)    


def collage_page(request):
    
    userdata = USER_DATA.objects.get(username = request.user.username)
    p_key=userdata.username
    return render(request,"davinci/collage.html",{'pk':p_key})

def collage_second_page(request,value):
    if(value=="0"):
        print('file length:' + str(len(request.FILES)))

        path_url = request.POST["path_url"].split("/")
        index_tile = path_url.index("collage") + 1
        layout = str(path_url[index_tile])
        path = "./static/gallery/data/"+ str(request.user.username)
             
        
        for i in range(len(request.FILES)):
            file_obj = request.FILES[str(i+1)]
            print(file_obj)
            path_temp = default_storage.save("collage/"+str(i+1) + '.png', ContentFile(file_obj.read()))

        files = glob("./media/collage/*.png")
        files.sort()
        if(layout == "tile_9-class"):
            tile_9(files,path)
        elif(layout == "tile_5-class"): 
            tile_5(files,path)  
        else:
            tile_4(files,path)          
        for j in files:
            os.remove(j)
        path_output = "./static/gallery/data/"+ str(request.user.username) + "/media/output/collage.png"
        with open(path_output, "rb") as image_file:
             encoded_string = base64.b64encode(image_file.read())
            
        encoded_string = str(encoded_string)[2:-1]    
        prefix = "data:image/png;base64,"
        encoded_string = prefix + encoded_string 
        data = {'val':"success",'url_output':encoded_string}
        return JsonResponse(data) 


    else:    
        value = value + ".png"
        print(value)
        site_url = "http://" + str(request.META['HTTP_HOST']) +"/static/gallery/images/" + value
    userdata = USER_DATA.objects.get(username = request.user.username)
    p_key=userdata.username
    return render(request,"davinci/collage_second.html",{'pk':p_key,'layout':site_url})   


def load_vault(request):
    val = int(request.POST["object"])
    if(val == None):
        val=4
    path = "./static/gallery/data/"+ str(request.user.username)
    files1 = glob(path+"/*.jpg")
    files2 = glob(path+"/*.png")
    files = files1 + files2
   
    
    if(len(files) < val):
        val = len(files)

    output = ""
    file_str = ""   
    for k in range(val):
        filename = files[k].split("/")[-1]
        file_str = file_str + filename + "::"
        
        path_output = files[k]
        with open(path_output, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            
        encoded_string = str(encoded_string)[2:-1]
        if(filename.split(".")[-1] == "jpg"):    
            prefix = "data:image/jpg;base64,"
        else:   
            prefix = "data:image/png;base64,"    
        encoded_string = prefix + encoded_string
        output = output + encoded_string + "**"

    output = output[0:-2] 
    file_str = file_str[0:-2]   

    data = {'val':"success",'url_output':output,'filename':file_str,'count':val}

    return JsonResponse(data)




def format_page_one(request,value=None):
    
    userdata = USER_DATA.objects.get(username = request.user.username)
    p_key=userdata.username

    if(value !=  None):
        print("value is" + str(value))
        site_url = "http://" + str(request.META['HTTP_HOST']) +"/static/gallery/images/"
        form_redirect_url = "http://" + str(request.META['HTTP_HOST']) + "/davinci/gallery/format/convert/" +value + "/"
        url_select =  site_url + str(value) + "_icon.png"
        return render(request,"davinci/format_second.html",{'pk':p_key,'url':url_select,'form_url':form_redirect_url})
 
    else:
        print("None: homepage")
        return render(request,"davinci/format_one.html",{'pk':p_key})              

def format_process(request,value=None):
    path = "./media/convert/"
    dirs = os.listdir(path)
    for i in dirs:
        os.remove(path+i)
    count = 0
   
    for i in request.FILES.getlist('file'):
        img = i
        count += 1
        path_temp = default_storage.save("convert/"+str(count) + '.' +value, ContentFile(img.read()))
   
    new_value = str(value) + "-" + str(count)
    return redirect("davinci:format_page_third",val=new_value) 

def format_page_third(request,val):
    userdata = USER_DATA.objects.get(username = request.user.username)
    p_key=userdata.username

    site_url = "http://" + str(request.META['HTTP_HOST']) +"/media/convert/"
    print(val)
    format_value = val.split("-")[0]
    count = int(val.split("-")[1])
    url_name = []
    for i in range(1,count+1):
        output = str(i) + "." + format_value
        url = site_url + output
        download_name = "output_"+ output
        data = (url,download_name)
        url_name.append(data)
    
    return render(request,"davinci/format_third.html",{'pk':p_key,'format':format_value,'img_data':url_name}) 
