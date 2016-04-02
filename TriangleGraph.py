from Shell import shell
from PIL import Image
from functools import partial
import multiprocessing
import time
import sys
import NaturalSelection
import Compare
import random
import profile
import os
import copy
import BreedShells
import pygame
from pygame.locals import *
############################
# Try SciPy module
############################

def select_index():
    correct_input = False
    while correct_input == False:
        try:
            input_idx = int(input('select the index'))
            correct_input = True
        except:
            print"Incorrect input, only number is accepted, please try again"
            sys.exc_clear()
    return input_idx

def main():
    global best_shell,screen,shell_list,process_num,generation,original_img,catastrophe_time,cache_massage
    while generation <= total_generation:

        print 'generation '+ str(generation)

        partial_compare = partial(Compare.compare, original_img=original_img)
        pool = multiprocessing.Pool(processes = process_num)
        shell_list = pool.map(partial_compare,shell_list)
        pool.close()
        pool.join()

        #print "generation: " + str(generation)

        NaturalSelection.rerange(shell_list)

        if generation == catastrophe_num*catastrophe_time*catastrophe_time:
            shell_list = NaturalSelection.catastrophe(shell_list)
            txt = open(file_name + '\\' + 'log.txt','a')
            txt.write("\nI am the cataclysm!\n\n")
            txt.close()
            catastrophe_time += 1
            print "\nI am the cataclysm!\n"

        shell_list = NaturalSelection.filtration(shell_list,shell_in_beach)

        cache_massage += str(generation) + ":" + str(shell_list[0].get_similarity()) + '\n'
        if shell_list[0].get_similarity() > last_similarity[0]:
            shell_list[0].save_img(generation,os.getcwd()+'\\' + file_name + '\\')
            last_similarity[0] = shell_list[0].get_similarity()
            best_shell = shell_list[0].get_img()
        elif generation % 50 == 0:
            shell_list[0].save_img(generation,os.getcwd()+'\\' + file_name + '\\')
            txt = open(file_name + '\\' + 'log.txt','a')
            txt.write(cache_massage)
            txt.close()
            cache_massage = ''

        #partial_breed_shells = partial(BreedShells.breed_shells, shell_in_beach=int(shell_in_beach/process_num))
        #pool = multiprocessing.Pool(processes = process_num)
        #new_shell_list = pool.map(partial_breed_shells,shell_list)
        #pool.close()
        #pool.join()
        #shell_list.extend(new_shell_list)
        shell_list.extend(BreedShells.breed_shells(shell_list,shell_in_beach))
        #print shell_list
        generation+=1


def savefile():
    global cache_massage,file_name,generation,catastrophe_time,shell_list
    txt = open(file_name + '\\' + 'log.txt','a')
    txt.write(cache_massage)
    txt.write('Evolution done.\n\n\n')
    txt.close()
    txt = open(file_name+'\\save.txt','w')
    txt.write(str(generation) + '\n' + str(catastrophe_time))
    for idx in xrange(len(shell_list)):
        txt.write('\n' + str(idx) + ":" + str(shell_list[idx].get_contain()))
    txt.close()

if __name__ == "__main__":
    try:
        last_time_passed = 0
        screen = None
        fps = 24
        best_shell = None
        clock = pygame.time.Clock()

        image_loc = "images"
        shell_list = []
        shell_in_beach = 70
        split_parts = 5.0
        error_range = 0.25
        img_size = (350,350)
        process_num = 7
        catastrophe_num = 9
        catastrophe_time = 1
        generation = 0
        catastrophe_generation = 100
        total_generation = 250000
        file_name = ''
        cache_massage = ''

        print "0.Start New.\n1.Load Save."
        option_idx = select_index()
        while type(option_idx) is not int or option_idx < 0 or option_idx >= 2:
            print"Not doable option, please try again"
            print "0.Start New.\n1.Load Save."
            option_idx = select_index()
        if option_idx == 0:
            ISOTIMEFORMAT='%Y-%m-%d %H-%M-%S'
            file_name = 'saves\\' + str(time.strftime(ISOTIMEFORMAT, time.localtime()))
            print('Creating new file ' + file_name)
            os.makedirs(file_name)
            file_list = [file_loc for file_loc in os.listdir(os.getcwd() + '\\' + image_loc) if ".jpg" in file_loc or ".png" in file_loc]
            for idx in xrange(0,len(file_list)):
                print str(idx) + '. ' + str(file_list[idx])
            original_img_idx = select_index()
            while type(original_img_idx) is not int or original_img_idx < 0 or original_img_idx >= len(file_list):
                print"Cannot open this image, please try again"
                for idx in xrange(0,len(file_list)):
                    print str(idx) + '. ' + str(file_list[idx])
                original_img_idx = select_index()

            print "Getting file " + file_list[original_img_idx] + '.....'
            original_img= Image.open(image_loc+'\\'+file_list[original_img_idx])
            f=open(file_name + '\\' + 'log.txt',"w")
            f.close()
            f=open(file_name + '\\' + 'save.txt',"w")
            f.close()
            original_img = original_img.resize(img_size)
            for idx in xrange(shell_in_beach):
                shell_list.append(shell(original_img.size,[]))
            last_similarity = [0.0,0]
            original_img.save(file_name + '\\original_img.png','png')
            print ".....done. Start main loop."
        elif option_idx == 1:
            file_list = [file_loc for file_loc in os.listdir(os.getcwd() + '\\saves') if "." not in file_loc]
            for idx in xrange(0,len(file_list)):
                print str(idx) + '. ' + str(file_list[idx])
            save_idx = select_index()
            while type(save_idx) is not int or save_idx < 0 or save_idx >= len(file_list):
                print"Cannot open this save, please try again"
                for idx in xrange(0,len(file_list)):
                    print str(idx) + '. ' + str(file_list[idx])
                save_idx = select_index()
            file_name = 'saves\\' + file_list[save_idx]
            print 'Loading save form ' + file_name + '.....'
            original_img= Image.open(file_name + '\\' + 'original_img.png')

            save = open(file_name + '\\save.txt','r')
            shell_triangles_list = []
            save_data = save.readlines()
            generation = int(save_data[0])
            catastrophe_time = int(save_data[1])
            for line_idx in xrange(2,len(save_data)):
                line = save_data[line_idx]
                cache_line = line[line.find(":")+1:]
                shell_list.append(shell(original_img.size,eval(cache_line)))
            last_similarity = [0.0,0]
            print ".....done. Start main loop."
        txt = open(file_name + '\\' + 'log.txt','a')
        txt.write('Start evolution.\n')
        txt.close()
        main()
        savefile()
    except:
        savefile()
