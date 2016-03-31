import random
from PIL import Image,ImageDraw
import sys
import os
import copy

class shell:
    triangle_num = 100
    mutation_probability = 0.3
    def __init__(self,shell_size,decided_triangle):
        self.founded = False
        self.similarity = 0.0
        self.advantage = 0.0
        self.accumulated_advantage = 0.0
        self.shell_size = shell_size
        self.contain = []
        self.Img = Image.new("RGB",self.shell_size,(255,255,255))
        self.contain = copy.deepcopy(decided_triangle)
        while len(self.contain) < self.triangle_num:
            #print self.triangle_num
            xyList = [[random.randint(0,self.shell_size[0]),random.randint(0,self.shell_size[1])] for idx in xrange(3)]
            color = [random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            self.contain.append((xyList,color))
        self.changed = True
        self.is_mutate()

    def is_changed(self):
        return self.changed

    def compared(self):
        self.changed = False

    def get_item(self, input_list,index):
        try:
            idx = random.randint(0,len(input_list)-1)
            index.append(idx)
            self.get_item(input_list[idx],index)
            return index
        except:
            sys.exc_clear()
            return index

    def mutate(self):
        self.changed = True
        if random.random() <=0.5:
            rand_idx,rand_jdx = random.randint(0,len(self.contain)-1),random.randint(0,len(self.contain)-1)
            self.contain[rand_idx],self.contain[rand_jdx] = self.contain[rand_jdx],self.contain[rand_idx]
        else:
            idx_list = self.get_item(self.contain,[])
            if len(idx_list) == 4:
                idx,jdx,kdx,ldx = idx_list
                self.contain[idx][jdx][kdx][ldx] = random.randint(0,255)
            else:
                idx,jdx,kdx = idx_list
                self.contain[idx][jdx][kdx] = random.randint(0,self.shell_size[0])

    def is_mutate(self):
        if random.random() <= self.mutation_probability:
            self.mutate()

    def get_size(self):
        return self.shell_size

    def drawShell(self):
        self.Img = Image.new("RGB",self.shell_size,(255,255,255))
        draw = ImageDraw.Draw(self.Img,'RGBA')
        for triangle in self.contain:
            #cache_Img = Image.new("RGBA",self.shell_size,0)
            #draw_on_cache = ImageDraw.Draw(cache_Img)
            #draw_on_cache.polygon(triangle[0],fill = triangle[1])
            draw.polygon([tuple(triangle[0][0]),tuple(triangle[0][1]),tuple(triangle[0][2])],fill = tuple(triangle[1]))
            #cache_Img_sp = cache_Img.convert("RGBA")
            #self.Img.paste(cache_Img,(0,0),mask = cache_Img)

    def get_contain(self):
        return self.contain

    def rebirth(self,contain):
        self.contain = copy.deepcopy(contain)
        self.is_mutate()

    def return_genes(self,loc):
        gene1 = self.contain[:loc]
        gene2 = self.contain[loc:]
        return [gene1,gene2]

    def save_img(self,generation,pic_path):
        #txt = open('list.txt','a')
        #txt.write(str(self.generation) + ":" + str(self.similarity) + '\n')
        #txt.close()
        self.Img.save(pic_path + str(generation) + "-" + str(self.similarity) + "%" + '.png',"png")

    def breed(self,other_shell,loc):
        first_genes = self.return_genes(loc)
        second_genes = other_shell.return_genes(loc)
        [first_genes[idx].extend(second_genes[1-idx]) for idx in xrange(2)]
        return [first_genes[idx] for idx in xrange(2)]

    def set_similarity(self,similarity):
        self.similarity = similarity

    def get_similarity(self):
        return self.similarity

    def set_advantage(self,advantage):
        self.advantage = advantage

    def get_advantage(self):
        return self.advantage

    def set_accumulated_advantage(self,accumulated_advantage):
        self.accumulated_advantage = accumulated_advantage

    def get_accumulated_advantage(self):
        return self.accumulated_advantage

    def found(self):
        self.founded = True

    def is_founded(self):
        return self.founded

    def get_img(self):
        self.drawShell()
        return self.Img
