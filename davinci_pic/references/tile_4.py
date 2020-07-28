from PIL import Image
from glob import glob
def tile_4(files,path):
#     files = glob('images/*.jpg')

    im_list = []

    for i in range(len(files)):
        im = Image.open(files[i])
        im = im.resize((500,500))
        img = Image.new('RGB',(520,520),(255,255,255))
        img.paste(im,(10,10))
        im_list.append(img)

    t_width = 1040
    t_height = 1040


    img = Image.new('RGB',(t_width,t_height),(255,255,255))
    k=0
    w = im_list[0].size[0]
    h = im_list[0].size[1]

    for i in range(0,h+1,h):
        for j in range(0,w+1,w):
            img.paste(im_list[k],(j,i))
            k+=1


    w = img.size[0]
    h = img.size[1]




    img_frame = Image.open("./references/frame.jpg")

    img_frame = img_frame.resize((t_width+100,t_height+100))

    img_frame.paste(img,(50,50))


    new_image = Image.new('RGBA',(t_width+500,t_height+500),(0,0,0,0))

    new_image.paste(img_frame,(200,200))

    new_image.save(path +"/media/output/collage.png")

      
