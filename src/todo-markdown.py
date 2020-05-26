import fileinput
import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import os
import re
import textwrap


class todo_markdown(kp.Plugin):
    """
    Manages todos in a Markdown file

    Plugin that gives you the ability to 
    add/finish/delete todos that are stored in a markdown file
    """

    TODO_CAT = kp.ItemCategory.USER_BASE + 10
    ADD_TODO_CAT = kp.ItemCategory.USER_BASE + 20

    FINISH_TODO_NAME = "finish"
    FINISH_TODO_LABEL = "Finish the Todo"

    DELETE_TODO_NAME = "delete"
    DELETE_TODO_LABEL = "Delete the Todo"

    _todos = []

    def __init__(self):
        super().__init__()

    def _read_config(self):
        settings = self.load_settings()

        # It's the folder FOLDERID_Documents ("%USERPROFILE%\Documents")
        # https://docs.microsoft.com/sv-se/windows/win32/shell/knownfolderid?redirectedfrom=MSDN
        default_path = kpu.shell_known_folder_path(
            "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}"
        )
        self._filepath = settings.get_stripped(
            "file_path", "main", default_path
        )

        if os.path.isdir(self._filepath):
            self._filepath = os.path.join(self._filepath, "todo.md")

    def on_start(self):
        self._debug = False
        self._read_config()

        self.set_actions(self.TODO_CAT, [
            self.create_action(
                name=self.FINISH_TODO_NAME,
                label=self.FINISH_TODO_LABEL,
                short_desc="Finish the todo"
            ),
            self.create_action(
                name=self.DELETE_TODO_NAME,
                label=self.DELETE_TODO_LABEL,
                short_desc="Removes the todo completely"
            ),
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
            target = user_input.strip().format(q=user_input.strip())
            suggestions.append(
                self.create_item(
                    category=self.ADD_TODO_CAT,
                    label="Add as todo: '{}'".format(user_input),
                    short_desc=target,
                    target=target,
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE,
                    loop_on_suggest=False
                )
            )

        self.set_suggestions(suggestions, kp.Match.DEFAULT, kp.Sort.NONE)

    def on_execute(self, item, action):
        if item.category() == self.ADD_TODO_CAT:
            self._add_todo(item.short_desc())

        if item and item.category() == self.TODO_CAT:
            if action and action.name() == self.FINISH_TODO_NAME:
                self._finish_todo(item.label())
            if action and action.name() == self.DELETE_TODO_NAME:
                self._delete_todo(item.label())

    def on_activated(self):
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                markdown = f.read()

                self._todos = []
                todos = self._fetch_all_open_todos(markdown)

                for todo in todos:
                    self._todos.append(self._create_suggestion(
                        todo.split("]")[1]
                    ))
        except FileNotFoundError as e:
            self.warn(e)

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self._read_config()

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
            self.err(e)

    def _add_todo(self, todo):
        try:
            with open(self._filepath, 'a+', encoding="utf-8") as f:
                f.write("\n- [ ] {}".format(todo))
        except Exception as e:
            self.err(e)

    def _delete_todo(self, todo):
        try:
            with open(self._filepath, 'r', encoding="utf-8") as f:
                newlines = []
                for line in f.readlines():
                    if todo not in line:
                        newlines.append(line)
            with open(self._filepath, 'w', encoding="utf-8") as f:
                for line in newlines:
                    f.write(line)
        except Exception as e:
            self.err(e)

    def _create_suggestion(self, item):

        text = textwrap.wrap(item, width=50)
        label = text.pop(0)

        return self.create_item(
            category=self.TODO_CAT,
            label=label,
            short_desc="".join(text),
            target=item.strip().format(q=item.strip()),
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.IGNORE,
        )
