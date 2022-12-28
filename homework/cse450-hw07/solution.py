def traversal(final, json_str):

    final.append(json_str['value'])
    json_str['order'] = len(final)

    if 'left' in json_str:
        traversal(final, json_str['left'])

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
    # Traverse the tree using pre-order depth-first order (i.e., root-left-right),
    # and add an integer element "order" into every node of the tree. The
    # value of the "order" element should indicate the order of traversal starting
    # from 1 (which is the root of the tree). Return a JSON object with the modified
    # tree. See the tests to better understand the requirements of the assignment.
    # For example, if the input tree is this:
    # {
    #    "value": 314,
    #    "left": {
    #        "value": 5
    #    },
    #    "right": {
    #         "value": 6
    #    }
    # }
    #
    # the output tree should be as follows:
    # {
    #     "value": 314,
    #     "left": {
    #         "value": 5,
    #         "order": 2
    #     },
    #     "right": {
    #         "value": 6,
    #         "order": 3
    #     },
    #     "order": 1
    # }    
    #
    # Assume the JSON string is always legitimate (i.e., no formating errors).

    import json

    json_string = json.loads(text)
    final = []

    traversal(final, json_string)

    return json_string
