
import erl_terms


def convert(script_content, env):
    return substitute_vars(erl_terms.decode(script_content), env)


def get_packages(mlist):
    if isinstance(mlist, list):
        if len(mlist) > 1 and mlist[0] == "require_package":
            return mlist[1:]
        else:
            return reduce(lambda a, x:a + get_packages(x), mlist, [])
    elif isinstance(mlist, tuple):
        return get_packages(list(mlist))
    else:
        return []


def substitute_vars(term_tree_root, env):

    def cast_to_type_of(value, default_value):
        type_name = 'atom'
        if isinstance(default_value, int):
            type_name = 'integer'
        elif isinstance(default_value, float):
            type_name = 'float'
        elif is_string_literal(default_value):
            type_name = 'string'
        return cast_to_type(value, type_name)

    def cast_to_type(value, type_name):
        if isinstance(value, str):
            if type_name == 'string':
                return value
            elif type_name == 'integer':
                return int(value)
        print("Couldn't convert {0} to type {1}".format(value, type_name))
        return value

    def is_string_literal(s):
        return isinstance(s, str)

    def is_atom(a):
        # erl_terms currently doesn't provide a way to distinguish atoms and strings
        return is_string_literal(a)

    def go(node):
        if isinstance(node, tuple):
            node_ = tuple(go(child) for child in node)
            if len(node_) > 1 and node_[0] == 'var':
                if is_string_literal(node_[1]):
                    var_name = node_[1]
                    if var_name in env:
                        if len(node_) == 2:
                            return env[var_name]
                        else:
                            return cast_to_type_of(env[var_name], node_[2])
                elif isinstance(node_[1], tuple) and len(node_[1]) == 2:
                    var_name, var_type_name = node_[1]
                    if is_string_literal(var_name) and is_atom(var_type_name) and var_name in env:
                        return cast_to_type(env[var_name], var_type_name)
            return node_
        elif isinstance(node, list):
            return [go(child) for child in node]
        return node

    return go(term_tree_root)


def get_includes(mlist):
    if isinstance(mlist, list):
        if len(mlist)>0 and mlist[0] == "include_resource":
            return [mlist[2]]
        else:
            return reduce(lambda a, x:a + get_includes(x), mlist, [])
    elif isinstance(mlist, tuple):
            return get_includes(list(mlist))
    else:
        return []