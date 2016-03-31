def split_image(img,split_parts):
    w,h = img.size
    pw = w/int(split_parts)
    ph = h/int(split_parts)
    return_list = []
    for idx in xrange (0, w, pw):
        for jdx in xrange(0, h, ph):
            return_list.append(img.crop((idx, jdx, idx+pw, jdx+ph)))
    return return_list

def hist_similar(new_img,old_img):
    original_img_histogram=old_img.histogram()
    shell_img_histogram=new_img.histogram()
    #set similarity of two histogram by using formaluer from http://blog.csdn.net/gzlaiyonghao/article/details/2325027
    #don't really understand how that work... needs learn more about this
    return sum(1 - (0 if o == n else float(abs(o - n))/max(o, n)) for o, n in zip(original_img_histogram, shell_img_histogram))/len(original_img_histogram)

def hash_similar(new_img):
    global old_img_key
    new_img_gray = new_img.convert('L').resize((9,8))
    new_img_key = []
    for idx in xrange(new_img_gray.size[0]):
        for jdx in xrange(new_img_gray.size[1]-1):
            if new_img_gray.getpixel((idx,jdx)) > new_img_gray.getpixel((idx,jdx+1)):
                new_img_key.append(1)
            else:
                new_img_key.append(0)
    cache_similarity = 0.0
    for idx in xrange(len(new_img_key)):
        if old_img_key[idx] == new_img_key[idx]:
            cache_similarity += 1.0
    return cache_similarity/64.0

def pix_similar(new_img,original_img):
    new_img_RGB = new_img.resize((int(new_img.size[0]/3),int(new_img.size[1]/2))).convert('RGB')
    old_img_RGB = original_img.resize((int(new_img.size[0]/3),int(new_img.size[1]/2))).convert('RGB')
    #new_img_RGB = new_img.convert('RGB')
    #old_img_RGB = original_img.convert('RGB')
    similarity_sum = sum(1.0-(abs(new_color - old_color)/255.0) for x in xrange(new_img_RGB.size[0]) for y in xrange(new_img_RGB.size[1])\
     for old_color,new_color in zip(old_img_RGB.getpixel((x,y)),new_img_RGB.getpixel((x,y))))
    return similarity_sum/(new_img_RGB.size[0]*new_img_RGB.size[1]*3.0)

def compare(shell,original_img):
    #print get_original_img().get_size()
    #Wtestinput = input('= =')
    #new_shell_list = []
    #for shell in shell_list:
    shell.is_mutate()
    if shell.is_changed():
        shell.set_similarity(100.0*pix_similar(shell.get_img(),original_img))
        shell.compared()
    return shell
    #    new_shell_list.append(shell)
    #return new_shell_list
