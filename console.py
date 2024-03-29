#!/usr/bin/python3

"""
Console program that contains the entry point of the
command interpreter.
Uses the cmd module and a custom prompt '(hbnb) '
"""


import cmd
import models
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand custom class to handle line-oriented commands
    Inherits from cmd.Cmd
    """
    prompt = "(hbnb) "
    class_dict = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, line):
        """Command to quit the program"""
        return True

    def do_EOF(self, line):
        """Command to check for 'EOF' and quit the program"""
        return True

    def default(self, line):
        """Default behavior for empty lines and unknown commands."""
        pass

    def do_create(self, args):
        """Creates a new instance of BaseModel"""
        if not args:
            print("** class name missing **")
            return

        arg = args.split(" ")
        className = arg[0]

        if className not in self.class_dict:
            print("** class doesn't exist **")
            return

        param_dict = {}
        for param in arg[1:]:
            try:
                key, value = param.split("=")
                value = value.replace("_", " ")\
                    .replace('\"', '').replace("\\", '')
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                elif '.' in value:
                    value = float(value)
                elif value.isdigit():
                    value = int(value)

                param_dict[key] = value
            except ValueError:
                pass

        # Create an instance of the specified class
        # with the parsed parameters
        my_model = HBNBCommand.class_dict[className](**param_dict)
        my_model.save()
        print(my_model.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        """

        if not arg:
            print("** class name missing **")
        else:
            try:
                args = arg.split(" ")
                className, obj_id = args
                try:
                    temp_name = ".".join([className, obj_id])
                    storage_keys = list(storage.all().keys())
                    if storage_keys:
                        storage_keys_split = storage_keys[0].split(".")
                        if temp_name in storage.all().keys():
                            instances = storage.all()[temp_name]
                            if instances:
                                print(instances)
                            else:
                                print("** no instance found **")
                        elif (className in self.class_dict.keys()):
                            print("** no instance found **")
                        else:
                            print("** class doesn't exist **")
                    else:
                        print("** no instance found **")
                except KeyError:
                    print("** class doesn't exist **")
            except ValueError:
                print("** instance id missing **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file)
        """
        if not arg:
            print("** class name missing **")
        else:
            try:
                args = arg.split(" ")
                className, obj_id = args
                try:
                    temp_name = ".".join([className, obj_id])
                    if temp_name in storage.all().keys():
                        del storage.all()[temp_name]
                    else:
                        print("** no instance found **")
                except KeyError:
                    print("** class doesn't exist **")
            except ValueError:
                print("** instance id missing **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name
        """
        className = arg if arg else None
        all_instances = storage.all()
        if className is not None:
            class_instances = [
                    str(instance) for instance in all_instances.values()
                    if instance.__class__.__name__ == className
                    ]
            if class_instances:
                print(class_instances)
            else:
                print("** no instance found **")
        else:
            print([str(instance) for instance in all_instances.values()])

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)
        """
        if not arg:
            print("** class name missing **")
        else:
            try:
                className, obj_id, attrKey, attrValue = arg.split(" ")
                main_key = ".".join([className, obj_id])
                if main_key in storage.all().keys():
                    instance = storage.all()[main_key]
                    if instance:
                        if (
                                attrKey == "id" or
                                attrKey == "created_at"
                                or attrKey == "updated_at"):
                            return
                        else:
                            setattr(instance, attrKey, attrValue)
                            instance.save()
                    else:
                        print("** no instance found **")
                else:
                    classNameId = list(storage.all().keys())
                    name_id, class_id = classNameId[0].split(".")
                    if className != name_id:
                        print("** class doesn't exist **")
                    else:
                        print("** no instance found **")
            except ValueError:
                args = arg.split(" ")
                if len(args) == 0:
                    print("** class name missing **")
                elif len(args) == 1:
                    print("** instance id missing **")
                elif len(args) == 2:
                    print("** attribute name missing **")
                else:
                    print("** value missing **")

    def help_quit(self):
        """Help function for quit"""
        print("Command to exit the program")
        print("Usage: quit")

    def help_EOF(self):
        """Help function for do_EOF"""
        print("Command to exit the program")
        print("Usage: $ 'ctrl+d' or $ 'EOF'.")

    def help_create(self):
        """Help function for do_create"""
        print("Function to create new instance of class object.")
        print("Usage: $ create <class name>")

    def help_show(self):
        """Help function for do_show"""
        print("Function to show the instance of a class object.")
        print("Usage: $ show <class name> <instance id>")

    def help_destroy(self):
        """Help function for do_destroy"""
        print("Function to destroy an instance of a class object.")
        print("Usage: $ destroy <class name> <instance id>")

    def help_all(self):
        """Help function for do_all"""
        print("Function to print all the instance of a class object.")
        print(":: If <class name> is not specified, prints instances.")
        print(
                ":: If <class name> is specified, "
                "prints all instances of the class"
                )
        print("Usage: $ all or $ all <class name> ")

    def help_update(self):
        """Help function for do_update"""
        print("Function to update the attrributes of an instance.")
        print(
                "To identify the instance to update, "
                "the class name and id are required."
                )
        print(
                "The attributes to be updated to the instance, "
                "in keys and values pair to are also required."
                )
        print(
                "Usage: $ update <class name> <instance id> "
                "<attribute key> <attribute value>"
                )


if __name__ == '__main__':
    HBNBCommand().cmdloop()
