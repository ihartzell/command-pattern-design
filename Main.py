# TODO: Isaac Hartzell
# TODO: June-10-2019
# TODO: This program demonstrates the command pattern design.
# TODO: --------------------------------------------------------------

# This is the global state string that all commands will act on.
globalStateStr = "halo3 is the best"


# This is an interface, although python doesn't really have interfaces
# this class simply defines the functions that all other commands will use without implementing them.
class Command(object):

    def exec(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


# This class gives the behavior for appending a letter to the end of a string.
class AppendLetterCommand(Command):
    def __init__(self, letter):
        self.letter = letter

    # This function appends a letter to the global string.
    def exec(self):
        global globalStateStr
        globalStateStr += self.letter

    # This function calls for the opposite command.
    def undo(self):
        undoManager.doCommand(DeleteLetterFromEndCommand())


# This class creates the behavior for deleting a letter from the beginning of a string.
class DeleteLetterFromStartCommand(Command):
    def __init__(self):
        global globalStateStr
        self.letter = globalStateStr[0] # String the beginning letter of the string to use in the undo function.

    # This function deletes the starting letter of the global string.
    def exec(self):
        global globalStateStr
        # Deletes the beginning letter from the string.
        globalStateStr = globalStateStr[1:]

    # This function performs the logic necessary for appending a letter to the start of the string
    # which is the opposite of this current command.
    def undo(self):
        global globalStateStr
        globalStateStr = globalStateStr[::-1]  # Reverses the global string.
        undoManager.doCommand(AppendLetterCommand(self.letter))  # Appends a letter to the end of the reversed string.
        globalStateStr = globalStateStr[::-1]  # Puts the string back to its original state.


# This class creates the behavior for deleting a letter from the end of a string.
class DeleteLetterFromEndCommand(Command):

    def __init__(self):
        self.letter = globalStateStr[-1]  # Storing the last letter of the string to use in the undo function.

    # This function removes the last letter of the global string.
    def exec(self):
        global globalStateStr
        globalStateStr = globalStateStr[:-1]

    # This function does the opposite of the DeleteLetterFromEndCommand
    def undo(self):
        undoManager.doCommand(AppendLetterCommand(self.letter))  # Here's where the letter comes into play as I have to
                                                                 # pass it a letter.


# This class creates the behavior for capitalizing a letter at any index of the string.
class CapitalizeLetterAtAnyIndexCommand(Command):
    def __init__(self, indexOfStr):
        self.indexOfStr = indexOfStr

    # This function capitalizes the string at a specific index.
    def exec(self):
        global globalStateStr
        globalStateStr = globalStateStr[:self.indexOfStr] + globalStateStr[self.indexOfStr].capitalize() + \
                      globalStateStr[self.indexOfStr + 1:]

    # This function will do the opposite of capitalizing a letter of a string at any index.
    def undo(self):
        undoManager.doCommand(LowerCaseLetterAtAnyIndexCommand(self.indexOfStr))


# This class creates the behavior for lower casing a letter at a specific index.
class LowerCaseLetterAtAnyIndexCommand(Command):
    def __init__(self, indexOfStr):
        self.indexOfStr = indexOfStr

    # This function will lower case a letter in the string specified by an index.
    def exec(self):
        global globalStateStr
        globalStateStr = globalStateStr[:self.indexOfStr] + globalStateStr[self.indexOfStr].lower() + \
                      globalStateStr[ self.indexOfStr + 1:]
        # This is an empty list that is used for the undo portion of the TitleCaseCommand.
        # This will be a list which stores each word in the whole global string.
        holdingList = []
        # I then append the global string to this list.
        holdingList.append(globalStateStr + ' ')

    # This function will undo what this command I'm in does.
    def undo(self):
        undoManager.doCommand(CapitalizeLetterAtAnyIndexCommand(self.indexOfStr))


# This class controls the behavior for giving the title case of the global string.
class TitleCaseCommand(Command):
    # This function will give the title case for the global string.
    def exec(self):
        global globalStateStr
        globalStateStr = globalStateStr.title()

    # This function undoes what the title case command does.
    def undo(self):
        for strElem in range(len(globalStateStr)):  # Cycle through every element in the global string.
            # If the element is 0, this makes it so the first
            # character of the first word in the string isn't missed or 1 from the element is a space, then
            # LowerCaseLetterAtAnyIndex gets called and the first word of the global string gets appended to
            # the empty list which is now in non-title-case format.
            if strElem is 0 or globalStateStr[strElem - 1] is ' ':
                undoManager.doCommand(LowerCaseLetterAtAnyIndexCommand(strElem))


# This class gives the behavior for all the undoing and redoing.
class UndoManager(object):
    # Creating two separate stacks being lists.
    def __init__(self):
        self.undoStack = []
        self.redoStack = []

    # This function pops the undo stack and stores this result in command.
    # It then puts this command onto the redo stack, and then the appropriate undo for the specific command is called.
    def undo(self):
        command = self.undoStack.pop()
        self.redoStack.append(command)
        command.undo()

    # This function pops the redo stack and stores it in command, then this command executes.
    # This redoes the initial command that happend.
    def redo(self):
        command = self.redoStack.pop()
        command.exec()

    # This function appends whatever command is passed onto the undoStack, and then the command passed into
    # this function is executed.
    def doCommand(self, command):
        self.undoStack.append(command)
        command.exec()


# Instance is global
undoManager = UndoManager()

if __name__ == '__main__':
    # Test case 1: AppendLetterCommand
    # --------------------------------------------------
    print("Test case 1: AppendLetterCommand")
    print("Current string -> ", globalStateStr)
    undoManager.doCommand(AppendLetterCommand('g'))
    print(globalStateStr)
    # Undo test
    undoManager.undo()
    print(globalStateStr)
    # Redo test
    undoManager.redo()
    print(globalStateStr, '\n')
    # Test case 2: DeleteLetterFromStartCommand
    # --------------------------------------------------
    print("Test case 2: DeleteLetterFromStartCommand")
    print("Current string -> ", globalStateStr)
    undoManager.doCommand(DeleteLetterFromStartCommand())
    print(globalStateStr)
    # Undo Test
    undoManager.undo()
    print(globalStateStr)
    # Redo Test
    undoManager.redo()
    print(globalStateStr, '\n')
    # Test case 3: DeleteLetterFromEndCommand
    # --------------------------------------------------
    print("Test case 3: DeleteLetterFromEndCommand")
    print("Current string -> ", globalStateStr)
    undoManager.doCommand(DeleteLetterFromEndCommand())
    print(globalStateStr)
    # Undo Test
    undoManager.undo()
    print(globalStateStr)
    # Redo Test
    undoManager.redo()
    print(globalStateStr, '\n')
    # Test case 4: CapitalizeLetterAtAnyIndexCommand
    # --------------------------------------------------
    print("Test case 4: CapitalizeLetterAtAnyIndexCommand")
    print("Current string -> ", globalStateStr)
    undoManager.doCommand(CapitalizeLetterAtAnyIndexCommand(5))
    print(globalStateStr)
    # Undo Test
    undoManager.undo()
    print(globalStateStr)
    # Redo Test
    undoManager.redo()
    print(globalStateStr, '\n')
    # Test case 5: LowerCaseLetterAtAnyIndexCommand
    # --------------------------------------------------
    print("Test case 5: LowerCaseLetterAtAnyIndexCommand")
    print("Current string -> ", globalStateStr)
    undoManager.doCommand(LowerCaseLetterAtAnyIndexCommand(5))
    print(globalStateStr)
    # Undo Test
    undoManager.undo()
    print(globalStateStr)
    # Redo Test
    undoManager.redo()
    print(globalStateStr, '\n')
    # Test case 6: TitleCaseCommand
    # --------------------------------------------------
    print("Test case 6: TitleCaseCommand")
    print("Current string -> ", globalStateStr)
    undoManager.doCommand(TitleCaseCommand())
    print(globalStateStr)
    # Undo Test
    undoManager.undo()
    print(globalStateStr)
    # Redo Test
    undoManager.redo()
    print(globalStateStr)
