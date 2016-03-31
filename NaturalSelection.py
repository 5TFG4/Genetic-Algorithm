import random
import Compare
import BreedShells

def rerange(shell_list):
    shell_list.sort(key = lambda shells:shells.get_similarity(), reverse=True)

def filtration(shell_list,shell_in_beach):
    #while len(shell_list) > shell_in_beach:
    #    for idx in range(random.randint(0,len(shell_list)/3))
    #        shell_list.pop()
    return shell_list[0:shell_in_beach]
    #print len(shell_list)

def catastrophe(shell_list):
    #print " I am the cataclysm!"
    return shell_list[random.randint(int(0.4*len(shell_list)),int(0.6*len(shell_list))):len(shell_list)]
