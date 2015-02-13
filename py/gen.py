#coding: utf-8
#!/usr/bin/python
"""
Eclipse.py by Bruce Eckel, for Thinking in Java 4e
Modify or insert package statments so that Eclipse is happy with the code tree.
Run this with no arguments from the root of the code tree.

The Ant build will not work once you run this program!

You may also want to modify the dotproject and dotclasspath text below.

You must have Python 2.3 installed to run this program. See www.python.org.
"""
import os
import Image as image

import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

con = ''


#裁剪压缩图片
def clipResizeImg(**args):
    
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
        
    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size
 
    dst_scale = float(arg['dst_h']) / arg['dst_w'] #目标高宽比
    ori_scale = float(ori_h) / ori_w #原高宽比
 
    if ori_scale >= dst_scale:
        #过高
        width = ori_w
        height = int(width*dst_scale)
 
        x = 0
        y = (ori_h - height) / 3
        
    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)
 
        x = (ori_w - width) / 2
        y = 0
 
    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None
 
    #压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])
    

i = 0
con2 = ''
for path, dirs, files in os.walk('.'):
    for file in files:
        
        if file.endswith(".jpg") and file.find('_')<0 :
            filepath = path + os.sep + file
            dst_img = filepath.replace('.jpg','_214_350.jpg')
            #clipResizeImg(ori_img=filepath,dst_img=dst_img,dst_w=214,dst_h=350,save_q=75)
            i = i + 1
            con = con+"""
  <div class="col-xs-6 col-md-3" >
    <a href="%s" id="%s" class="thumbnail" >
      <img src="%s"  alt="...">
      <div class="caption">
        <h3>%s</h3>
      </div>
    </a>
    
  </div>
  """%(file,'id_'+str(i),file.replace('.jpg','_214_350.jpg'),file[0:10])
            con2 = con2 + """
  			<li class="">
               <a href="#%s">%s</a>
			</li>
  			"""%('id_'+str(i),file.replace('.jpg',''))

open("gen3.txt", 'w').write(con)
open("gen4.txt", 'w').write(con2)