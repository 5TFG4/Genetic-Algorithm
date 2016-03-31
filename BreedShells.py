import random
from Shell import shell

def random_select_shell(shell_list):
    selected_idx = random.random()
    for shells in shell_list:
        if shells.get_accumulated_advantage()-shells.get_advantage() <= selected_idx <= shells.get_accumulated_advantage():
            return shells

def breed_shells(shell_list,shell_in_beach):
    new_shell_list = []
    shell_similarity_sum = 0.0
    for shells in shell_list:
        shell_similarity_sum += shells.get_similarity()
    accumulated_advantage = 0.0
    for shells in shell_list:
        cache_advantage = shells.get_similarity()/shell_similarity_sum
        accumulated_advantage += cache_advantage
        shells.set_advantage(cache_advantage)
        shells.set_accumulated_advantage(accumulated_advantage)
    #del_shell_list = []
    #while len(shell_list)+len(new_shell_list) <= shell_in_beach:
    for idx in range(random.randint(0,shell_in_beach/2)):
        changed_shell = [random_select_shell(shell_list),random_select_shell(shell_list)]
        for new_shell_triangles in changed_shell[0].breed(changed_shell[1],random.randint(0,len(changed_shell[0].get_contain())-1)):
            new_shell_list.append(shell(changed_shell[0].get_size(),new_shell_triangles))
    return new_shell_list
