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





#   TODO: Checkout MovieDB plugin! It has manage to get about the structure I want


import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

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
    ADD_TODO = kp.ItemCategory.USER_BASE + 20

    _todos = [
            
    ]


    def __init__(self):
        super().__init__()


    def on_start(self):
        #kp.live_package_dir # Find out where the live package dir is
        #kp.shell_execute # Executes/opens file. Might be used to open the markdown-file
        self._debug = True

        self._todos = [
            self.create_item(
                category=self.TODO_CAT,
                label="Fix 'Add Todo'",
                short_desc="",
                target="todo_1",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE,
            ),
            self.create_item(
                category=self.TODO_CAT,
                label="Fix 'Delete' Todo",
                short_desc="It should be an action",
                target="todo_2",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE,
            ),
            self.create_item(
                category=self.TODO_CAT,
                label="Add Finish action",
                short_desc="",
                target="todo_3",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE,
            ),
            self.create_item(
                category=self.TODO_CAT,
                label="Add a 'Assign to another' action",
                short_desc="It will copy and delete",
                target="todo_4",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE,
            ),
            self.create_item(
                category=self.TODO_CAT,
                label="What happens if they have the same target?",
                short_desc="They need different targets otherwise they are not shown",
                target="todo_5",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE,
            ),
            self.create_item(
                category=self.TODO_CAT,
                label="Test having a 'load more'",
                short_desc="Do we want to encurage that behavior. Maybe a setting?",
                target="todo_6",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE,
            ),
        ]

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
        
        if items_chain == self.TODO_CAT:
            self.dbg("items_chain", items_chain[0])
            self.dbg("user_input", user_input)
            self.dbg("------------")


        if not items_chain:
            return
        
        suggestions = self._todos

        if user_input:
            target = user_input.strip().format(q = user_input.strip())
            suggestions.append(
                self.create_item(
                    category=self.ADD_TODO,
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
        pass

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass
