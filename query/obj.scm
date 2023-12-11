(function_definition
    type: (_) @return_type
    [(pointer_declarator
    (function_declarator
        (identifier) @func_name
        (parameter_list) @param_list))
    (function_declarator
        (identifier) @func_name
        (parameter_list) @param_list)])

(method_definition
    (method_type) @return_type
    . (identifier) @func_name
    [(identifier)
    (method_parameter) @param_list]*)

(method_declaration
    (method_type) @return_type
    . (identifier) @func_name
    [(identifier)
    (method_parameter) @param_list]*)