def traversal(final, json_str):

    if 'left' in json_str:
        traversal(final, json_str['left'])

    final.append(json_str['value'])

    if 'right' in json_str:
        traversal(final, json_str['right'])

def question01(text):
    # The argument of this function is a JSON string.
    # The corresponding JSON object is a binary tree, each node of which
    # has the following format:
    #
    # {
    #   "value": <VALUE>,        
    #   "left": <LEFT_BRANCH>,
    #   "right": <RIGHT_BRANCH>
    # }
    #
    # where <LEFT_BRANCH> and <RIGHT_BRANCH> are nodes,
    # and each <VALUE> is an integer. If "left" or "right" do not exist,
    # then the node does not have corresponding branches. Intuitively,
    # a node with both "left" and "right" keys absent is a leaf.
    # 
    # Return the list of values obtained by in-order depth-first traversal 
    # of the tree (i.e., left-root-right) See the tests to better understand 
    # the requirements of the assignment.
    #
    # Assume the JSON string is always legitimate (i.e., no formating errors).

    import json

    json_string = json.loads(text)
    final = []

    traversal(final, json_string)

    return final