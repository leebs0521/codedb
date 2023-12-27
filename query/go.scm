; 일반 함수
(function_declaration
 name: (identifier) @func_name
 parameters: (parameter_list) @param_list
 result: (type_identifier)? @return_type
 result: (parameter_list)? @return_type
 result: (qualified_type)? @return_type
 result: (slice_type)? @return_type
 result: (interface_type)? @return_type
 result: (map_type)? @return_type)

; 클래스 메소드
(method_declaration
  receiver: (parameter_list)
  name: (field_identifier) @func_name
  parameters: (parameter_list) @param_list
  result: (type_identifier)? @return_type
  result: (parameter_list)? @return_type
  result: (qualified_type)? @return_type
  result: (slice_type)? @return_type
  result: (interface_type)? @return_type
  result: (map_type)? @return_type)
