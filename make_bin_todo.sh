#!/bin/bash  
# Make a directory at ~/bin. Add this path to ~.bashrc and put all the commands related to ToDo programs into that directory.

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
dir="bin"

# Make directory at $HOME
echo "Making directory $dir in \$HOME.."
mkdir ~/$dir

# Copying all todo commands 
echo "Creating utility commands.."
ln -s $SCRIPTPATH/"add_tasks.py" ~/$dir/addtask
ln -s $SCRIPTPATH/"activate_categorise.sh" ~/$dir/categorize
ln -s $SCRIPTPATH/"mark_tasks.py" ~/$dir/marktask
ln -s $SCRIPTPATH/"show_tasks.py" ~/$dir/showtask
echo "Done!!"


# Add export path command to bashrc
echo "Adding directory to path in .bashrc .."
echo "export PATH=\$PATH:$HOME/$dir" >> ~/.bashrc

echo "Restart your shell for the features to start working.."