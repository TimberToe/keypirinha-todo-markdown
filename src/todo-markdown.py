# Keypirinha launcher (keypirinha.com)

# 
#    In on_start I should 
#     - Read config
#
#    In on_catalog I should
#     - Read the Markdown file? 
#       # Might be heavy on each on_catalog.  Needs to be more often than on_start though...
#     - Add to the catalog:
#       - Todo
#         - Add
#         - Finish
#         - List
#         - Open file
#
#   In on_events I should:
#    - Scan the markdown file since the config has changed
#
#   In on_suggest under:
#    - "Todo" I should
#      - List the top todos
#    - "Add" I should search todos so that I can see if I'm about to add a double todo
#       - The top item should always be an "add new todo" that will be executed on enter
#    - "Finish" I should search todos to find the one I want to finich
#    - "List" I should directly show a list of *all* todos (if possible)
#    - "Open file" I should open the markdown file in default editor
#   
#   In on_execute I should
#    - If under "Finish" I should finish the todo
#    - If under "Add" I should only add a new todo on the "add new todo" otherwise to nothing
#    - If under "List" I should do nothing on enter
#    - If under "actions for an item" these actions should be visible:
#        - Delete
#        - Finish
#        - (Keypirinhas normal ones should not be listed)






import fileinput
import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import re

class todo_markdown(kp.Plugin):
    """
    One-line description of your plugin.

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    More detailed documentation at: http://keypirinha.com/api/plugin.html

    """
    
    TODO_CAT = kp.ItemCategory.USER_BASE + 10
    ADD_TODO_CAT = kp.ItemCategory.USER_BASE + 20

    FINISH_TODO_NAME = "finish"
    FINISH_TODO_LABEL = "Finish the Todo"

    DELETE_TODO_NAME = "delete"
    DELETE_TODO_LABEL = "Delete the Todo"
    
    EDIT_TODO_NAME = "edit"
    EDIT_TODO_LABEL = "Edit the Todo"

    _todos = [
            
    ]

    _filepath = "c:\TEST\keypirinha-todo-markdown\sample.md"

    def __init__(self):
        super().__init__()


    def on_start(self):
        #kp.live_package_dir # Find out where the live package dir is
        #kp.shell_execute # Executes/opens file. Might be used to open the markdown-file
        self._debug = True

        self.set_actions(self.TODO_CAT,[
            self.create_action(
                name=self.FINISH_TODO_NAME,
                label=self.FINISH_TODO_LABEL,
                short_desc="Finish the todo"
            ),
            self.create_action(
                name=self.DELETE_TODO_NAME,
                label=self.DELETE_TODO_LABEL,
                short_desc="Deletes the todo completly"
            ),
            self.create_action(
                name=self.EDIT_TODO_NAME,
                label=self.EDIT_TODO_LABEL,
                short_desc="Edits the todo"
            )
        ])


    def on_catalog(self):
        catalog = []

        catalog.append(self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label="Todo",
            short_desc="Manages todos",
            target="todo",
            args_hint=kp.ItemArgsHint.REQUIRED,
            hit_hint=kp.ItemHitHint.KEEPALL
        ))

        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):


        if not items_chain:
            return
        
        suggestions = self._todos[:]

        if user_input:
            target = user_input.strip().format(q = user_input.strip())
            suggestions.append(
                self.create_item(
                    category=self.ADD_TODO_CAT,
                    label = "Add '{}' as todo".format(user_input),
                    short_desc=target,
                    target=target,
                    args_hint = kp.ItemArgsHint.FORBIDDEN,
                    hit_hint = kp.ItemHitHint.IGNORE,
                    loop_on_suggest = False
                )
            )

        self.set_suggestions(suggestions, kp.Match.DEFAULT, kp.Sort.NONE)

    def on_execute(self, item, action):
        if item.category() == self.ADD_TODO_CAT:
            self.dbg("CREATE TODO")
            self._add_todo(item.short_desc())

        if item and item.category() == self.TODO_CAT:
            self.dbg(item.label())
            if action and action.name() == self.FINISH_TODO_NAME:
                self.dbg("Finish TODO")
                self._finish_todo(item.label())
            if action and action.name() == self.DELETE_TODO_NAME:
                self.dbg("Delete TODO")
            if action and action.name() == self.EDIT_TODO_NAME:
                self.dbg("Edit TODO")


    def on_activated(self):
        with open(self._filepath, "r", encoding="utf-8") as f:
            markdown = f.read()

            self._todos = []
            todos = self._fetch_all_open_todos(markdown)
            
            for todo in todos:
                self._todos.append(self._create_suggestion(
                    todo.split("]")[1]
                ))

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass

    def _fetch_all_todos(self, markdown):
        regex = r'\[[[Xx ]*\].+'
        return re.findall(regex, markdown)

    def _fetch_all_open_todos(self, markdown):
        regex = r'\[[[ ]*\].+'
        return re.findall(regex, markdown)

    def _finish_todo(self, todo):
        try:
            with open(self._filepath, 'r', encoding="utf-8") as f:
                newlines = []
                for line in f.readlines():
                    if todo in line:
                        newlines.append(line.replace("[ ]", "[X]", 1))
                    else:
                        newlines.append(line)

            with open(self._filepath, 'w', encoding="utf-8") as f:
                for line in newlines:
                    f.write(line)
        except Exception as e:
            print("Error:", e)

    def _add_todo(self, todo):
        try:
            with open(self._filepath, 'a', encoding="utf-8") as f: 
                f.write("\n- [ ] {}".format(todo))
        except Exception as e:
            print("Error", e)

    def _create_suggestion(self, item):
        return self.create_item(
            category = self.TODO_CAT,
            label = item,
            short_desc = "",
            target = item.strip().format(q = item.strip()),
            args_hint = kp.ItemArgsHint.FORBIDDEN,
            hit_hint = kp.ItemHitHint.IGNORE,
        )