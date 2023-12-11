static void *parser__push(Parser *self, StackVersion version, Tree *tree,
                         TSStateId state) {}

static bool parser__breakdown_top_of_stack(Parser *self, StackVersion version) {
  bool did_break_down = false;
  bool pending = false;

  do {
    StackPopResult pop = ts_stack_pop_pending(self->stack, version);
    if (!pop.slices.size)
      break;

    did_break_down = true;
    pending = false;
    for (uint32_t i = 0; i < pop.slices.size; i++) {
      StackSlice slice = pop.slices.contents[i];
      TSStateId state = ts_stack_top_state(self->stack, slice.version);
      Tree *parent = *array_front(&slice.trees);

      for (uint32_t j = 0; j < parent->child_count; j++) {
        Tree *child = parent->children[j];
        pending = child->child_count > 0;

        if (child->symbol == ts_builtin_sym_error) {
          state = ERROR_STATE;
        } else if (!child->extra) {
          state = ts_language_next_state(self->language, state, child->symbol);
        }

        ts_stack_push(self->stack, slice.version, child, pending, state);
      }

      for (uint32_t j = 1; j < slice.trees.size; j++) {
        Tree *tree = slice.trees.contents[j];
        parser__push(self, slice.version, tree, state);
      }

      LOG("breakdown_top_of_stack tree:%s", SYM_NAME(parent->symbol));
      LOG_STACK();

      ts_stack_decrease_push_count(self->stack, slice.version,
                                   parent->child_count + 1);
      ts_tree_release(parent);
      array_delete(&slice.trees);
    }
  } while (pending);

  return did_break_down;
}