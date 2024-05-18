#!/usr/bin/python3
"""
Module for console
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


def split_curly_braces(e_arg):
    """
    Splits the curly braces for the update method.
    """
    curly_braces = re.search(r"\{(.*?)\}", e_arg)
    if curly_braces:
        id_with_comma = shlex.split(e_arg[:curly_braces.span()[0]])
        obj_id = [i.strip(",") for i in id_with_comma][0]
        str_data = curly_braces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + str_data + "}")
        except Exception:
            print("** invalid dictionary format **")
            return
        return obj_id, arg_dict
    else:
        commands = e_arg.split(",")
        if commands:
            try:
                obj_id = commands[0].strip()
                attr_name = commands[1].strip()
                attr_value = commands[2].strip()
                return obj_id, f"{attr_name} {attr_value}"
            except IndexError:
                pass
    return "", ""


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity", "Place", "Review", "State", "City"]

    def emptyline(self):
        pass

    def do_EOF(self, arg):
        return True

    def do_quit(self, arg):
        return True

    def do_create(self, arg):
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{commands[0]}()")
            storage.new(new_instance)
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(commands[0], commands[1])
            objects = storage.all()
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(commands[0], commands[1])
            objects = storage.all()
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        commands = shlex.split(arg)
        objects = storage.all()
        if len(commands) == 0:
            for obj in objects.values():
                print(str(obj))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, obj in objects.items():
                if key.startswith(commands[0]):
                    print(str(obj))

    def do_count(self, arg):
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == commands[0])
            print(count)

    def do_update(self, arg):
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(commands[0], commands[1])
            objects = storage.all()
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                attr_name = commands[2]
                attr_value = commands[3]
                try:
                    attr_value = eval(attr_value)
                except Exception:
                    pass
                setattr(obj, attr_name, attr_value)
                obj.save()

    def default(self, arg):
        arg_list = arg.split('.')
        cls_name = arg_list[0]
        command = arg_list[1].split('(')
        cmd_method = command[0]
        e_arg = command[1].split(')')[0]
        method_dict = {
            'all': self.do_all,
            'show': self.do_show,
            'destroy': self.do_destroy,
            'update': self.do_update,
            'count': self.do_count
        }
        if cmd_method in method_dict:
            if cmd_method != "update":
                return method_dict[cmd_method](f"{cls_name} {e_arg}")
            else:
                try:
                    obj_id, arg_dict = split_curly_braces(e_arg)
                    return method_dict[cmd_method](f"{cls_name} {obj_id} {arg_dict}")
                except Exception:
                    pass
        else:
            print(f"*** Unknown syntax: {arg}")
            return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
