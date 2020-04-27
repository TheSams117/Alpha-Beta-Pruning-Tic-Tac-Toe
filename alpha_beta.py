def is_game_over(node):
    winning_indexes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    for indexes in winning_indexes:
        hit_count = 0
        chosen_symbol = node[indexes[0]]

        for index in indexes:
            if node[index] is not None and node[index] == chosen_symbol:
                hit_count = hit_count + 1

        if hit_count == 3:
            return True, chosen_symbol

    if node.count(None) == 0:
        return True, None

    return False, None

def generate_children(node, chosen_symbol): # TODO: Create a function to generate the children states for minimax evaluation
    childrens = []
    count = 0
    for i in node:
        if i is None:
            temp = node[0:9]
            temp[count] = chosen_symbol
            childrens.append(temp)
        count = count+1

    return childrens

def alternate_symbol(symbol):
    return 'o' if symbol == 'x' else 'x'

def mini_max_ab(node, is_maximizing_player_turn, chosen_symbol,alpha,beta): # TODO: Modify this minimax in order to turn it into an alpha-beta pruning version with depth cutting
    
    game_result = is_game_over(node)

    if game_result[0]:
        if game_result[1] is None:
            return 0, node

        return (-1, node) if is_maximizing_player_turn else (1, node)

    children = generate_children(node, chosen_symbol)
    if(is_maximizing_player_turn):
        maxEval = -2
        childToWin = []
        for child in children:
            eval = mini_max_ab(child,False,alternate_symbol( chosen_symbol),alpha,beta)
            if(maxEval<eval[0]):
                childToWin = child
                maxEval = eval[0]
            
            if(alpha<eval[0]):
                alpha = eval[0]

            if (beta <= alpha):
                break
        return maxEval,childToWin
    else:
        minEval = 2
        childToWin = []
        for child in children:
            eval = mini_max_ab(child,True,alternate_symbol( chosen_symbol),alpha,beta)

            if(minEval>eval[0]):
                childToWin = child
                minEval = eval[0]

            if(beta>eval[0]):
                beta = eval[0]

            if (beta <= alpha):
                break
        return minEval,childToWin

def mini_max(node, is_maximizing_player_turn, chosen_symbol):
    game_result = is_game_over(node)

    if game_result[0]:
        if game_result[1] is None:
            return 0, node

        return (-1, node) if is_maximizing_player_turn else (1, node)

    children = generate_children(node, chosen_symbol)
    children_results = list(map(
        lambda child: [
            mini_max(child, not is_maximizing_player_turn, alternate_symbol(chosen_symbol))[0],
            child
        ],
        children
    ))

    return max(children_results, key=str) if is_maximizing_player_turn else min(children_results, key=str)
