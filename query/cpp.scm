; 클래스 메소드
(_
 (storage_class_specifier)* @return_type
 [(primitive_type) @return_type
  (type_identifier) @return_type
  (sized_type_specifier) @return_type
  (qualified_identifier) @return_type
  (template_type) @return_type]
 (function_declarator
  (qualified_identifier
   (namespace_identifier)
   (identifier) @func_name)
 (parameter_list) @param_list))

; 클래스 포인터 메소드
(_
 (storage_class_specifier)* @return_type
 [(primitive_type) @return_type
  (type_identifier) @return_type
  (sized_type_specifier) @return_type
  (qualified_identifier) @return_type
  (template_type) @return_type]
 (pointer_declarator
  (function_declarator
   (qualified_identifier
    (namespace_identifier)
    (identifier) @func_name)
 (parameter_list) @param_list)))

; 일반 함수
(_
 (storage_class_specifier)* @return_type
 [(primitive_type) @return_type
  (type_identifier) @return_type
  (sized_type_specifier) @return_type
  (qualified_identifier) @return_type
  (template_type) @return_type]
 (function_declarator
  [(identifier) @func_name
   (field_identifier) @func_name]
  (parameter_list) @param_list))

; 포인터 함수
(_
 (storage_class_specifier)* @return_type
 [(primitive_type) @return_type
  (type_identifier) @return_type
  (sized_type_specifier) @return_type
  (qualified_identifier) @return_type
  (template_type) @return_type]
 (pointer_declarator
  (function_declarator
   [(identifier) @func_name
    (field_identifier) @func_name]
   (parameter_list) @param_list)))



