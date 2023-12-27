; 포인터 함수
(_
 (storage_class_specifier)* @return_type
 [type: (primitive_type) @return_type
  type: (type_identifier) @return_type
  type: (sized_type_specifier) @return_type]
 declarator: (pointer_declarator
  declarator: (function_declarator
   declarator: (identifier) @func_name
   parameters: (parameter_list) @param_list))
 )
; 일반 함수
(_
 (storage_class_specifier)* @return_type
 [type: (primitive_type) @return_type
  type: (type_identifier) @return_type
  type: (sized_type_specifier) @return_type]
 declarator: (function_declarator
  declarator: (identifier) @func_name
  parameters: (parameter_list) @param_list)
 )

